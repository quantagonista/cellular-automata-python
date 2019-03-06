class CrystalRule:
    @staticmethod
    def get_rules(seed):
        return {
            '00': int(seed[0]),
            '01': int(seed[1]),
            '02': int(seed[2]),
            '03': int(seed[3]),
            '04': int(seed[4]),
            '10': int(seed[5]),
            '11': int(seed[6]),
            '12': int(seed[7]),
            '13': int(seed[8]),
            '14': int(seed[9]),
        }


class WolframRules:
    @staticmethod
    def get_rules(seed):
        return {
            0: int(seed[7]),
            1: int(seed[6]),
            2: int(seed[5]),
            3: int(seed[4]),
            4: int(seed[3]),
            5: int(seed[2]),
            6: int(seed[1]),
            7: int(seed[0]),
        }
