levels = []

def makeLvls():
    l1()
    l2()

def l1():
    l1 = []
    l1_0 = [".                  ",
            "WWWWWWW            ",
            "W     W            ",
            "G     WWWWWWW      ",
            "B           WWWWWWW",
            "R  .         11111R",
            "M           WWWWWWW",
            "Y     WWWWWWW      ",
            "W     W            ",
            "WWWWWWW            ",
            "                  .",
            "(1_90_[-12,-3]|)"]
    l1.append(l1_0)

    l1_1 = [".      ",
            "GWWWWWW",
            "G22222R",
            "GWWWWWW",
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
            "(3_0_[-5,0]|)"]
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
            "(2_180_[5,0]|4_270_[0,0]|)"]
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
            "(3_90_[0,0]|5_90_[0,0]|)"]
    l1.append(l1_4)

    l1_5 = [".       ",
            "GBBBBBBW",
            "G  44  W",
            "G  44  W",
            "G  WW66W",
            "G  WW66W",
            "G      W",
            "G      W",
            "GGGGGGGG",
            "       .",
            "(4_270_[0,0]|6_0_[0,0]|)"]
    l1.append(l1_5)

    l1_6 = [".       ",
            "RRRRRRRW",
            "B  77  W",
            "B  77  W",
            "B  WW55W",
            "B  WW55W",
            "B      W",
            "B      W",
            "BGGGGGGG",
            "       .",
            "(5_180_[0,0]|7_90_[0,0]|)"]
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
            "(6_270_[0,0]|8_0_[-4,1]|)"]
    l1.append(l1_7)

    l1_8 = [".                  ",
            "WWWWWWW            ",
            "W     W            ",
            "G     WWWWWWW      ",
            "B           WWWWWWW",
            "R            11111R",
            "M           WWWWWWW",
            "Y     WWWWWWW      ",
            "W999  W            ",
            "W  WWWW            ",
            "W  WWWW            ",
            "W  WWWW            ",
            "W  WWWW            ",
            "W  WWWW            ",
            "GGGGWWW            ",
            "                  .",
            "(1_90_[-12,0]|)"]
    l1.append(l1_8)

    levels.append(l1)

def l2():
    l2 = []
    l3 = []
    l2_0 = [".                  ",
            "WWWWWWWRRRRWWW     ",
            "W            W     ",
            "W            W     ",
            "W       W    WGGGGG",
            "W            G1    ",
            "W  .          1    ",
            "W            G1    ",
            "W       W    WGGGGG",
            "W            W     ",
            "W            W     ",
            "WWWWWWWBBBBWWW     ",
            "                  .",
            "(1_90_[-13,-1]|)"]
    
    l2_1 = [".                  ",
            "         WWWWW     ",
            "     GGGGGWW GGGGG ",
            "GGGGGG     W     GG",
            "G      222 W      G",
            "G      222WWW     G",
            "G      222 W      G",
            "GGGGGG     W     GG",
            "     GGGGGWW GGGGG ",
            "         WWWWW     ",
            "                  .",
            "(2_90_[0,0]|3_0_[0,0]|4_270_[0,0]|5_180_[0,0]|)"]

    l2_2 = [".                  ",
            "         WWWWW     ",
            "     GGGGG333GGGGG ",
            "GGGGGG    333    GG",
            "G          W      G",
            "G         RWWWWWWWG",
            "G          W      G",
            "GGGGGG     W     GG",
            "     GGGGGWW GGGGG ",
            "         WWWWW     ",
            "                  .",
            "(3_0_[0,0]|4_270_[0,0]|5_180_[0,0]|)"]

    l2_3 = [".                  ",
            "         WWWWW     ",
            "     GGGGG   GGGGG ",
            "GGGGGG           GG",
            "G          B 444  G",
            "G         RWW444  G",
            "G          W 444  G",
            "GGGGGG     W     GG",
            "     GGGGG WWGGGGG ",
            "         WWWWW     ",
            "                  .",
            "(4_270_[0,0]|5_180_[0,0]|)"]
    
    l2_4 = [".                  ",
            "         WWWWW     ",
            "     GGGGG   GGGGG ",
            "GGGGGG           GG",
            "G          B      G",
            "G         RWY     G",
            "G          W      G",
            "GGGGGG    555    GG",
            "     GGGGG555GGGGG ",
            "         WWWWW     ",
            "                  .",
            "(5_180_[0,0]|)"]
    
    l2_5 = [".                  ",
            "         WWWWW     ",
            "     GGGGG   GGGGG ",
            "GGGGGG6          GG",
            "G     6    B      G",
            "      6   RWY     G",
            "G     6    M      G",
            "GGGGGG6          GG",
            "     GGGGG    GGGGG",
            "         WWWWW     ",
            "                  .",
            "(6_270_[13,1]|)"]
    
    l2_6 = [".                               ",
            "WWWWWWWR  RWWW                  ",
            "W            W        WWWWW     ",
            "W            W    GGGGG   GGGGG ",
            "W       R    WGGGGG           GG",
            "W           7G          B      G",
            "W           7          RWY     G",
            "W           7G          M      G",
            "W       W    WGGGGG           GG",
            "W            W    GGGGG   GGGGG ",
            "W            W        WWWWW     ",
            "WWWWWWWBBBBWWW                  ",
            "                               .",
            "(7_270_[0,5]|)"]
    
    l2_7 = [".             ",
            "      R    R  ",
            "      R    R  ",
            "      R    R  ",
            "      R    R  ",
            "      R0000R  ", 
            "WWWWWWWR  RWWW",
            "W            W",
            "W            W",
            "W       R    W",
            "W            G",
            "W            Y",
            "W            G",
            "W       W    W",
            "W            W",
            "W            W",
            "WWWWWWWBBBBWWW",
            "             .",
            "(0*3_180_[-3,7]|)"]

    l3_0 = [".           ",
            "WWWWWWWWWWWW",
            "     RR     ",
            "     RR     ",
            "RRRR1MM2RRRR",
            "   M    M   ",
            "   R    R   ",
            "   R    R   ",
            "   R    R   ",
            "   R    R   ",
            "   R    R   ",
            "   R    R   ",
            "   R    R   ", 
            "   WRRRRW   ",
            "           .",
            "(1_180_[10,8]|2_180_[0,1])|"]

    l3_1 = [".               ",
            "WWWWWWWWWWWW    ",
            "     RR         ",
            "     RR         ",
            "RRRR1MM2RRRR    ",
            "   M    M       ",
            "   R    R       ",
            "   R    R       ",
            "   R    R       ",
            "   R    RWWWWWWW",
            "   R           R",
            "   R           R",
            "   R    RRRRRR M", 
            "   WRRRRW     W ",
            "               .",
            "(1_180_[10,8]|2_180_[0,1])|"]

    l3_2 = [".                          ",
            "           WWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWW        3      ",
            "     RR             MRRRRRR",
            "     RR             MRRR   ",
            "RRRR MM RRRR        4  W   ",
            "       W   RRRRRRRRRR  W   ",
            "                    R  W   ",
            "                    R  W  .",
            "(3_90_[-19,1]|4_90_[-8,3])|"]

    l3_3 = [".                     ",
            "      WWWWWWWWWWWWWWWW",
            "WWWWWWW        5      ",
            "W              MRRRRRR",
            "WMRRRRR        MRRR   ",
            "      R        6  W   ",
            "      RRRRRRRRRR  W   ",
            "               R  W   ",
            "               R  W   ",
            "                     .",
            "(5_90_[-13,9]|6_90_[-8,-3])|"]

    l3_4 = [".               ",
            "WWWWWWWWWWWW    ",
            "     RR         ",
            "     RR         ",
            "RRRR1MM2RRRR    ",
            "   M    M       ",
            "   R    R       ",
            "   R    R  MMRRR",
            "   R    R  W   W",
            "   R    RWWWR  W",
            "   R           W",
            "   R           W",
            "   R    RRRRRRRW", 
            "   WRRRRW       ",
            "               .",
            "(1_180_[10,8]|2_180_[0,1])|"]
    
    l3_5 = [".                ",
            "     WWWWWWWWWWWW",
            "          RR     ",
            "          RR     ",
            "     RRRR1MM2RRRR",
            "        M    M   ",
            "        R    R   ",
            "        R    R   ",
            "        R    R   ",
            "        R    R   ",
            "WWWWWWWWR    R   ",
            "W            R   ",
            "RMRRRRRRR    R   ", 
            "        WRRRRW   ",
            "            .",
            "(1_180_[5,8]|2_180_[-5,1])|"]

    l3_6 = [".             ",
            "       MRRR   ",
            "      W   W   ",
            "       R  W   ",
            "       R  W   ",
            "       R  W   ", 
            "WWWWWWWR  RWWW",
            "W      8888  W",
            "W            W",
            "W       R    W",
            "W            G",
            "W            Y",
            "W            G",
            "W       B    W",
            "W            W",
            "W            W",
            "WWWWWWWBBBBWWW",
            "             .",
            "(8*2_0_[0,-5]|)"]

    l2_8 = [".             ",
            "WWWWWWWRYYRWWW",
            "W            W",
            "W            W",
            "W       R    W",
            "W            G",
            "W            Y",
            "W            G",
            "W       B    W",
            "W            W",
            "W            W",
            "WWWWWWWB  BWWW",
            "       G99R   ",
            "       G  R   ",
            "       G  R   ",
            "       G  R   ",
            "       G  R   ",
            "       G  R   ",
            "             .",
            "(9_0_[0,0]|)"]

    l2.append(l2_0)
    l2.append(l2_1)
    l2.append(l2_2)
    l2.append(l2_3)
    l2.append(l2_4)
    l2.append(l2_5)
    l2.append(l2_6)
    l2.append(l2_7)
    l2.append(l2_8)

    l3.append(l3_0)
    l3.append(l3_1)
    l3.append(l3_2)
    l3.append(l3_3)
    l3.append(l3_4)
    l3.append(l3_5)
    l3.append(l3_6)

    levels.append(l2)
    levels.append(l3)
