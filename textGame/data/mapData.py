class LevelList:
    levels = []

    def __init__(self):
        self.l1()

    def l1(self):
        l1 = []
        l1_0 = [".                  ",
                "WWWWWWW            ",
                "W     W            ",
                "W     WWWWWWW      ",
                "W           WWWWWWW",
                "W            11111R",
                "W           WWWWWWW",
                "W     WWWWWWW      ",
                "W     W            ",
                "WWWWWWW            ",
                "                  .",
                "(1_90_[-12,0]|)"]
        l1.append(l1_0)

        l1_1 = [".      ",
                "GGWWWWW",
                "G22222R",
                "GGWWWWW",
                "      .",
                "(2_270_[0,0]|)"]
        l1.append(l1_1)

        l1_2 = [".            ",
                "GGWWWWWWWWWWW",
                "G           W",
                "GGWWWW      W",
                "     WWWWW33W",
                "        WW33W",
                "     G      W",
                "     G      W",
                "     GRRRRRRR",
                "            .",
                "(3_180_[-5,0]|)"]
        l1.append(l1_2)

        l1_3 = [".       ",
                "WWWWWWWW",
                "W      W",
                "G      W",
                "G  WW22W",
                "G  WW22W",
                "G  44  W",
                "G  44  W",
                "GRRRRRRR",
                "       .",
                "(2_0_[5,0]|4_270_[0,0])"]
        l1.append(l1_3)

        l1_4 = [".       ",
                "BBBBBBBW",
                "G  55  W",
                "G  55  W",
                "G  WW  W",
                "G  WW  W",
                "G  33  W",
                "G  33  W",
                "GRRRRRRR",
                "       .",
                "(3_90_[0,0]|5_90[0,0])"]
        l1.append(l1_4)

        l1_5 = [".       ",
                "BBBBBBBW",
                "B  44  W",
                "B  44  W",
                "B  WW  W",
                "B  WW  W",
                "B  66  W",
                "B  66  W",
                "BGGGGGGG",
                "       .",
                "(4_270_[0,0]|6_270_[0,0])"]
        l1.append(l1_5)

        l1_6 = [".       ",
                "RRRRRRRW",
                "B  77  W",
                "B  77  W",
                "B  WW  W",
                "B  WW  W",
                "B  55  W",
                "B  55  W",
                "BGGGGGGG",
                "       .",
                "(5_90_[0,0]|7_90_[0,0])"]
        l1.append(l1_6)

        l1_7 = [".       ",
                "RRRRRRRW",
                "B  66  W",
                "B  66  W",
                "B  WW  W",
                "B   W  W",
                "B   W  W",
                "B   W  W",
                "BWWWW88W",
                "    W88W",
                "    W88W",
                "    W88W",
                "    W88W",
                "    GGGG",
                "       .",
                "(6_270_[0,0]|8_180_[-4,2])"]
        l1.append(l1_7)

        l1_8 = [".                  ",
                "WWWWWWW            ",
                "W     W            ",
                "G     WWWWWWW      ",
                "G           WWWWWWW",
                "G            11111R",
                "G           WWWWWWW",
                "G     WWWWWWW      ",
                "W000  W            ",
                "W  WWWW            ",
                "W  WWWW            ",
                "W  WWWW            ",
                "W  WWWW            ",
                "W  WWWW            ",
                "GGGGWWW            ",
                "                  .",
                "(1_90_[-12,0]|0_0_[0,0])"]
        l1.append(l1_8)

        self.levels.append(l1)
