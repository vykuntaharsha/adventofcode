raw_binary_map = """0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
A = 1010
B = 1011
C = 1100
D = 1101
E = 1110
F = 1111"""

binary_map = {}
for line in raw_binary_map.splitlines():
    [b, v] = line.split(" = ")
    binary_map[b] = v


def get_binary_string(s):
    return "".join([binary_map[c] for c in s])


class Packet:
    def __init__(self, version, _id) -> None:
        self.version = version
        self._id = _id
        self.packets = []
        self.value = None


def parse_packet(binary_string):
    b_version = binary_string[0:3]
    b_id = binary_string[3:6]

    version = int(b_version, 2)
    _id = int(b_id, 2)

    packet = Packet(version, _id)

    new_string = binary_string[6:]
    new_packets = []
    if _id == 4:
        # Literal Value
        b_string = ""
        while True:
            next_5_bits = new_string[:5]
            b_string += next_5_bits[1:]
            new_string = new_string[5:]
            if next_5_bits[0] == "0":
                # last
                packet.value = int(b_string, 2)
                break
    else:
        # Operator
        l_type = new_string[0]
        new_string = new_string[1:]
        if l_type == '0':
            # length of subpackets
            b_subpackets_len = new_string[:15]
            subpackets_len = int(b_subpackets_len, 2)
            new_string = new_string[15:]

            while subpackets_len > 0 and new_string:
                prev_len = len(new_string)
                sub_packet, new_string = parse_packet(new_string)
                curr_len = len(new_string)
                subpackets_len -= prev_len - curr_len
                new_packets.append(sub_packet)
        else:
            # number of subpackets
            num_of_subpackets = int(new_string[:11], 2)
            new_string = new_string[11:]

            while num_of_subpackets > 0 and new_string:
                sub_packet, new_string = parse_packet(new_string)
                num_of_subpackets -= 1
                new_packets.append(sub_packet)

    for p in new_packets:
        packet.packets.append(p)
    return packet, new_string


def count_versions(packet):
    count = packet.version
    for p in packet.packets:
        count += count_versions(p)
    return count


def calculate_packet_value(packet):
    if packet._id == 0:
        value = 0
        for p in packet.packets:
            value += calculate_packet_value(p)
        packet.value = value
    elif packet._id == 1:
        value = 1
        for p in packet.packets:
            value *= calculate_packet_value(p)
        packet.value = value
    elif packet._id == 2:
        packet.value = min([calculate_packet_value(p) for p in packet.packets])
    elif packet._id == 3:
        packet.value = max([calculate_packet_value(p) for p in packet.packets])
    elif packet._id == 5:
        sub1 = packet.packets[0]
        sub2 = packet.packets[1]
        packet.value = 1 if (
            calculate_packet_value(sub1) > calculate_packet_value(sub2)
        ) else 0
    elif packet._id == 6:
        sub1 = packet.packets[0]
        sub2 = packet.packets[1]
        packet.value = 1 if (
            calculate_packet_value(sub1) < calculate_packet_value(sub2)
        ) else 0
    elif packet._id == 7:
        sub1 = packet.packets[0]
        sub2 = packet.packets[1]
        packet.value = 1 if (
            calculate_packet_value(sub1) == calculate_packet_value(sub2)
        ) else 0

    return packet.value


if __name__ == "__main__":
    input = "E20D7880532D4E551A5791BD7B8C964C1548CB3EC1FCA41CC00C6D50024400C202A65C00C20257C008AF70024C00810039C00C3002D400A300258040F200D6040093002CC0084003FA52DB8134DE620EC01DECC4C8A5B55E204B6610189F87BDD3B30052C01493E2DC9F1724B3C1F8DC801E249E8D66C564715589BCCF08B23CA1A00039D35FD6AC5727801500260B8801F253D467BFF99C40182004223B4458D2600E42C82D07CC01D83F0521C180273D5C8EE802B29F7C9DA1DCACD1D802469FF57558D6A65372113005E4DB25CF8C0209B329D0D996C92605009A637D299AEF06622CE4F1D7560141A52BC6D91C73CD732153BF862F39BA49E6BA8C438C010E009AA6B75EF7EE53BBAC244933A48600B025AD7C074FEB901599A49808008398142013426BD06FA00D540010C87F0CA29880370E21D42294A6E3BCF0A080324A006824E3FCBE4A782E7F356A5006A587A56D3699CF2F4FD6DF60862600BF802F25B4E96BDD26049802333EB7DDB401795FC36BD26A860094E176006A0200FC4B8790B4001098A50A61748D2DEDDF4C6200F4B6FE1F1665BED44015ACC055802B23BD87C8EF61E600B4D6BAD5800AA4E5C8672E4E401D0CC89F802D298F6A317894C7B518BE4772013C2803710004261EC318B800084C7288509E56FD6430052482340128FB37286F9194EE3D31FA43BACAF2802B12A7B83E4017E4E755E801A2942A9FCE757093005A6D1F803561007A17C3B8EE0008442085D1E8C0109E3BC00CDE4BFED737A90DC97FDAE6F521B97B4619BE17CC01D94489E1C9623000F924A7C8C77EA61E6679F7398159DE7D84C015A0040670765D5A52D060200C92801CA8A531194E98DA3CCF8C8C017C00416703665A2141008CF34EF8019A080390962841C1007217C5587E60164F81C9A5CE0E4AA549223002E32BDCEA36B2E100A160008747D8B705C001098DB13A388803F1AE304600"

    b_string = get_binary_string(input)
    packet, s = parse_packet(b_string)
    print(count_versions(packet))
    print(calculate_packet_value(packet))
