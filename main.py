import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from music21 import *
from collections import Counter
import io
import pretty_midi
from scipy.io import wavfile
import os


notes_in_int = {'6.11.0': 0,
                '8.1': 1,
                '5.7.10.1': 2,
                '10.11.3.6': 3,
                '11.0.2': 4,
                'B4': 5,
                'D1': 6,
                'B-1': 7,
                '10.0.5': 8,
                '7.9.1': 9,
                '5.8.10': 10,
                '3.5': 11,
                '10.1.3.6': 12,
                'B-0': 13,
                '5.6.10': 14,
                '9.1.2': 15,
                'A7': 16,
                '10.11.3.5': 17,
                '7.9.11': 18,
                '11.1.4': 19,
                '11.2.5': 20,
                '0.2.4.5': 21,
                '9.10': 22,
                '1.3.8': 23,
                '2.8': 24,
                '8.10.1': 25,
                'C2': 26,
                '7.10.1': 27,
                '9.2': 28,
                '9.11.1': 29,
                '4.5.7.9.11.0': 30,
                'C#4': 31,
                '11.1.6': 32,
                'A1': 33,
                'D5': 34,
                '2.5': 35,
                'B2': 36,
                '4.8': 37,
                'E7': 38,
                '3.4.9': 39,
                '10.1.3': 40,
                '0.5.6': 41,
                '1.2.4': 42,
                '1.4.7.9': 43,
                '9.1.4': 44,
                '0.3.5.8': 45,
                '3.5.10': 46,
                '3': 47,
                '0.1': 48,
                '4.7.9': 49,
                '4.5.7': 50,
                '5.9.10': 51,
                '10.0.3': 52,
                '4.5.7.9': 53,
                '4.5.7.9.11': 54,
                'B0': 55,
                '0.4.5': 56,
                '8.0': 57,
                '0.3.7': 58,
                '0.2': 59,
                'G7': 60,
                '1': 61,
                '11.0.4': 62,
                '6.9.1': 63,
                '7.8.0.3': 64,
                'C1': 65,
                '9': 66,
                '9.11.1.4': 67,
                '10.1.5': 68,
                'E-6': 69,
                '5.6.9.0': 70,
                'B-3': 71,
                'C4': 72,
                '3.7.10': 73,
                '0.2.4': 74,
                '8.9.1': 75,
                '0.3.5': 76,
                'G#3': 77,
                '6': 78,
                '6.8.10': 79,
                '5.6.8': 80,
                '2.6': 81,
                '1.3.6.8': 82,
                '4.7.9.0': 83,
                '4.6.11': 84,
                '6.8.0': 85,
                '1.4.6': 86,
                'E-4': 87,
                '5.7.10': 88,
                '6.9.11': 89,
                'B6': 90,
                'E-7': 91,
                '3.7.8.10': 92,
                'A2': 93,
                '11.2.4.6.7': 94,
                '8.10.3': 95,
                '2.7': 96,
                '1.2.6.8': 97,
                '8.11.2': 98,
                '7.8': 99,
                '6.9': 100,
                '3.6.10': 101,
                '2.4.7': 102,
                '2.4.5.7': 103,
                '2.4.6.9': 104,
                '9.10.3': 105,
                '6.10.11': 106,
                '4.7.8': 107,
                '9.11.2.4': 108,
                '2.6.9': 109,
                '0.5': 110,
                '11.0.2.4.5.7.9': 111,
                '1.3.6': 112,
                '7.10.0': 113,
                '3.6.8.10': 114,
                '7.10.2': 115,
                '11.3.5': 116,
                'F1': 117,
                'F5': 118,
                '7.9.2': 119,
                '0.4.5.7': 120,
                'F7': 121,
                '11.0': 122,
                'E3': 123,
                '9.11.4': 124,
                'F#5': 125,
                '2.6.10': 126,
                '4.8.9': 127,
                '6.8.11': 128,
                '5.10.11': 129,
                'E-3': 130,
                '10.1': 131,
                '8.0.1': 132,
                'A4': 133,
                '2.3.7': 134,
                'B-5': 135,
                '4.6.9.0': 136,
                '0.2.4.5.7.9': 137,
                '4.5.9': 138,
                '8.11.3': 139,
                '9.0.3': 140,
                '7.9.10': 141,
                'F#4': 142,
                '0.4': 143,
                'G5': 144,
                '2.5.7': 145,
                '7.9': 146,
                '11.0.5': 147,
                '10.2.3': 148,
                '7.9.0': 149,
                'B-2': 150,
                '8.10.0': 151,
                'A5': 152,
                '0.2.6': 153,
                'E-1': 154,
                '3.6.8': 155,
                '8.10': 156,
                'D6': 157,
                '11.3.6': 158,
                '6.7.11': 159,
                '4.9': 160,
                'F6': 161,
                '3.4.8.10': 162,
                '11.3': 163,
                '9.1.2.4': 164,
                '11.2.4': 165,
                '4.6.9': 166,
                'C#6': 167,
                '2.3.4.5.7.9.11': 168,
                '0.4.7': 169,
                '1.2.6': 170,
                '7': 171,
                '7.0': 172,
                '11.2.6': 173,
                '1.3.5': 174,
                '11.1.3': 175,
                'G2': 176,
                '8.9': 177,
                '7.11.2': 178,
                '2.4.6': 179,
                '5.9.0': 180,
                'B-6': 181,
                'B7': 182,
                '11.1': 183,
                '0.1.5': 184,
                '11.2': 185,
                '8': 186,
                '4': 187,
                '10.0.2.5': 188,
                '11.1.2': 189,
                'E-2': 190,
                '9.0.4': 191,
                '4.10': 192,
                '0.1.2': 193,
                '10.2': 194,
                '4.7': 195,
                '9.1': 196,
                '1.5.7': 197,
                '10.2.5': 198,
                '2.4.9': 199,
                '6.9.0': 200,
                '3.6.8.11': 201,
                '3.7.8': 202,
                '8.11.1.4': 203,
                'C#5': 204,
                '2.3': 205,
                '5.6.11': 206,
                '6.8.11.1': 207,
                '7.10': 208,
                '1.4.6.9': 209,
                'G4': 210,
                '5.9': 211,
                '3.6': 212,
                '6.8.1': 213,
                '4.6': 214,
                '0.3.6': 215,
                '7.11': 216,
                'F3': 217,
                '6.11': 218,
                '10.1.4': 219,
                '9.11': 220,
                '2': 221,
                '2.5.7.9': 222,
                '1.5': 223,
                '2.3.6': 224,
                '4.5': 225,
                '9.10.2': 226,
                'C#2': 227,
                'F#6': 228,
                '0': 229,
                '1.4.6.7': 230,
                '5.7.11': 231,
                'G#2': 232,
                '5.7': 233,
                '0.2.5': 234,
                '8.11.1': 235,
                '2.5.9': 236,
                '10.2.4': 237,
                'C#1': 238,
                'F2': 239,
                '7.8.0': 240,
                '4.6.7': 241,
                'B-7': 242,
                'G6': 243,
                '4.8.9.11': 244,
                '5.6': 245,
                'C5': 246,
                '5.7.0': 247,
                '9.1.3': 248,
                '5.8.10.1': 249,
                '3.6.9': 250,
                '10.11.1.3.6': 251,
                '6.9.11.2': 252,
                '8.0.3': 253,
                'G1': 254,
                '9.11.0': 255,
                '9.10.2.3': 256,
                '7.10.0.3': 257,
                '8.9.11': 258,
                '5.7.9.11.0': 259,
                '1.2': 260,
                '2.7.8': 261,
                '3.8.9': 262,
                '7.9.11.0': 263,
                'C#3': 264,
                '0.2.4.7': 265,
                '4.6.8.11': 266,
                '4.9.10': 267,
                '8.10.2': 268,
                'C6': 269,
                '0.3': 270,
                'A3': 271,
                'C3': 272,
                '3.5.7': 273,
                '6.10': 274,
                'D7': 275,
                '1.4.7': 276,
                'A6': 277,
                '5.10': 278,
                '4.6.10': 279,
                '1.5.6.8': 280,
                '9.10.0': 281,
                'E-5': 282,
                '2.6.7': 283,
                '9.11.3': 284,
                '1.6': 285,
                '9.0.2': 286,
                'F4': 287,
                '0.4.8': 288,
                '0.6': 289,
                '9.0': 290,
                'E6': 291,
                '5.7.9.0': 292,
                '4.7.8.11': 293,
                'D3': 294,
                '5.6.10.11': 295,
                '11': 296,
                '3.5.9': 297,
                '4.7.10': 298,
                '8.9.0.3': 299,
                '1.4.8': 300,
                '4.7.9.11.0': 301,
                '4.8.11': 302,
                'E5': 303,
                '6.7': 304,
                '8.11': 305,
                '5.7.10.0': 306,
                '8.10.11': 307,
                'E1': 308,
                '11.0.4.7': 309,
                'E4': 310,
                '11.3.4': 311,
                '8.9.0': 312,
                '3.9': 313,
                'B5': 314,
                '3.8': 315,
                '7.11.0': 316,
                '6.7.9': 317,
                'G#7': 318,
                'F#7': 319,
                '10.11': 320,
                '1.5.9': 321,
                '6.8.10.2': 322,
                'B3': 323,
                '10.11.3': 324,
                '2.5.8': 325,
                '3.7': 326,
                '5.9.11': 327,
                '6.7.0': 328,
                '10.3.4': 329,
                '10.0': 330,
                '2.3.8': 331,
                '8.1.2': 332,
                '2.4': 333,
                '5.8.10.0': 334,
                '2.5.7.10': 335,
                '5.11': 336,
                '11.4': 337,
                '10.3': 338,
                '10': 339,
                '4.7.11': 340,
                '3.6.9.11': 341,
                '2.5.8.10': 342,
                '6.10.1': 343,
                '2.6.7.9': 344,
                'F#2': 345,
                '3.5.7.10': 346,
                '5.6.10.1': 347,
                'C7': 348,
                '2.4.8': 349,
                '9.1.4.5': 350,
                '0.2.3': 351,
                '7.0.1': 352,
                '6.8': 353,
                '5': 354,
                '5.8.0': 355,
                'G#5': 356,
                'G#6': 357,
                '0.2.4.5.7': 358,
                'G#4': 359,
                '1.4': 360,
                '11.2.5.7': 361,
                '3.5.8': 362,
                '5.8.11': 363,
                '10.0.2': 364,
                '1.3': 365,
                'B-4': 366,
                '9.0.2.5': 367,
                '6.8.9': 368,
                '5.7.9': 369,
                '3.7.11': 370,
                '2.3.7.10': 371,
                '2.4.5.7.9.11': 372,
                '0.2.7': 373,
                '11.3.5.6': 374,
                'G3': 375,
                '11.0.2.4.5.7': 376,
                '11.1.5': 377,
                '1.5.6': 378,
                '9.11.0.2': 379,
                '4.6.8': 380,
                'D4': 381,
                '1.5.8': 382,
                '9.11.2': 383,
                '7.11.0.2': 384,
                'D2': 385,
                '5.8': 386,
                '4.6.9.11': 387,
                '5.7.9.11': 388,
                '3.4': 389,
                'E2': 390,
                '2.4.5': 391,
                'B1': 392,
                'C#7': 393,
                '7.9.11.2': 394,
                'F#3': 395,
                '8.11.2.4': 396,
                '1.7': 397,
                '0.2.5.7': 398,
                '4.5.9.0': 399,
                'F#1': 400,
                'G#1': 401}

int_in_notes = {0: '6.11.0',
                1: '8.1',
                2: '5.7.10.1',
                3: '10.11.3.6',
                4: '11.0.2',
                5: 'B4',
                6: 'D1',
                7: 'B-1',
                8: '10.0.5',
                9: '7.9.1',
                10: '5.8.10',
                11: '3.5',
                12: '10.1.3.6',
                13: 'B-0',
                14: '5.6.10',
                15: '9.1.2',
                16: 'A7',
                17: '10.11.3.5',
                18: '7.9.11',
                19: '11.1.4',
                20: '11.2.5',
                21: '0.2.4.5',
                22: '9.10',
                23: '1.3.8',
                24: '2.8',
                25: '8.10.1',
                26: 'C2',
                27: '7.10.1',
                28: '9.2',
                29: '9.11.1',
                30: '4.5.7.9.11.0',
                31: 'C#4',
                32: '11.1.6',
                33: 'A1',
                34: 'D5',
                35: '2.5',
                36: 'B2',
                37: '4.8',
                38: 'E7',
                39: '3.4.9',
                40: '10.1.3',
                41: '0.5.6',
                42: '1.2.4',
                43: '1.4.7.9',
                44: '9.1.4',
                45: '0.3.5.8',
                46: '3.5.10',
                47: '3',
                48: '0.1',
                49: '4.7.9',
                50: '4.5.7',
                51: '5.9.10',
                52: '10.0.3',
                53: '4.5.7.9',
                54: '4.5.7.9.11',
                55: 'B0',
                56: '0.4.5',
                57: '8.0',
                58: '0.3.7',
                59: '0.2',
                60: 'G7',
                61: '1',
                62: '11.0.4',
                63: '6.9.1',
                64: '7.8.0.3',
                65: 'C1',
                66: '9',
                67: '9.11.1.4',
                68: '10.1.5',
                69: 'E-6',
                70: '5.6.9.0',
                71: 'B-3',
                72: 'C4',
                73: '3.7.10',
                74: '0.2.4',
                75: '8.9.1',
                76: '0.3.5',
                77: 'G#3',
                78: '6',
                79: '6.8.10',
                80: '5.6.8',
                81: '2.6',
                82: '1.3.6.8',
                83: '4.7.9.0',
                84: '4.6.11',
                85: '6.8.0',
                86: '1.4.6',
                87: 'E-4',
                88: '5.7.10',
                89: '6.9.11',
                90: 'B6',
                91: 'E-7',
                92: '3.7.8.10',
                93: 'A2',
                94: '11.2.4.6.7',
                95: '8.10.3',
                96: '2.7',
                97: '1.2.6.8',
                98: '8.11.2',
                99: '7.8',
                100: '6.9',
                101: '3.6.10',
                102: '2.4.7',
                103: '2.4.5.7',
                104: '2.4.6.9',
                105: '9.10.3',
                106: '6.10.11',
                107: '4.7.8',
                108: '9.11.2.4',
                109: '2.6.9',
                110: '0.5',
                111: '11.0.2.4.5.7.9',
                112: '1.3.6',
                113: '7.10.0',
                114: '3.6.8.10',
                115: '7.10.2',
                116: '11.3.5',
                117: 'F1',
                118: 'F5',
                119: '7.9.2',
                120: '0.4.5.7',
                121: 'F7',
                122: '11.0',
                123: 'E3',
                124: '9.11.4',
                125: 'F#5',
                126: '2.6.10',
                127: '4.8.9',
                128: '6.8.11',
                129: '5.10.11',
                130: 'E-3',
                131: '10.1',
                132: '8.0.1',
                133: 'A4',
                134: '2.3.7',
                135: 'B-5',
                136: '4.6.9.0',
                137: '0.2.4.5.7.9',
                138: '4.5.9',
                139: '8.11.3',
                140: '9.0.3',
                141: '7.9.10',
                142: 'F#4',
                143: '0.4',
                144: 'G5',
                145: '2.5.7',
                146: '7.9',
                147: '11.0.5',
                148: '10.2.3',
                149: '7.9.0',
                150: 'B-2',
                151: '8.10.0',
                152: 'A5',
                153: '0.2.6',
                154: 'E-1',
                155: '3.6.8',
                156: '8.10',
                157: 'D6',
                158: '11.3.6',
                159: '6.7.11',
                160: '4.9',
                161: 'F6',
                162: '3.4.8.10',
                163: '11.3',
                164: '9.1.2.4',
                165: '11.2.4',
                166: '4.6.9',
                167: 'C#6',
                168: '2.3.4.5.7.9.11',
                169: '0.4.7',
                170: '1.2.6',
                171: '7',
                172: '7.0',
                173: '11.2.6',
                174: '1.3.5',
                175: '11.1.3',
                176: 'G2',
                177: '8.9',
                178: '7.11.2',
                179: '2.4.6',
                180: '5.9.0',
                181: 'B-6',
                182: 'B7',
                183: '11.1',
                184: '0.1.5',
                185: '11.2',
                186: '8',
                187: '4',
                188: '10.0.2.5',
                189: '11.1.2',
                190: 'E-2',
                191: '9.0.4',
                192: '4.10',
                193: '0.1.2',
                194: '10.2',
                195: '4.7',
                196: '9.1',
                197: '1.5.7',
                198: '10.2.5',
                199: '2.4.9',
                200: '6.9.0',
                201: '3.6.8.11',
                202: '3.7.8',
                203: '8.11.1.4',
                204: 'C#5',
                205: '2.3',
                206: '5.6.11',
                207: '6.8.11.1',
                208: '7.10',
                209: '1.4.6.9',
                210: 'G4',
                211: '5.9',
                212: '3.6',
                213: '6.8.1',
                214: '4.6',
                215: '0.3.6',
                216: '7.11',
                217: 'F3',
                218: '6.11',
                219: '10.1.4',
                220: '9.11',
                221: '2',
                222: '2.5.7.9',
                223: '1.5',
                224: '2.3.6',
                225: '4.5',
                226: '9.10.2',
                227: 'C#2',
                228: 'F#6',
                229: '0',
                230: '1.4.6.7',
                231: '5.7.11',
                232: 'G#2',
                233: '5.7',
                234: '0.2.5',
                235: '8.11.1',
                236: '2.5.9',
                237: '10.2.4',
                238: 'C#1',
                239: 'F2',
                240: '7.8.0',
                241: '4.6.7',
                242: 'B-7',
                243: 'G6',
                244: '4.8.9.11',
                245: '5.6',
                246: 'C5',
                247: '5.7.0',
                248: '9.1.3',
                249: '5.8.10.1',
                250: '3.6.9',
                251: '10.11.1.3.6',
                252: '6.9.11.2',
                253: '8.0.3',
                254: 'G1',
                255: '9.11.0',
                256: '9.10.2.3',
                257: '7.10.0.3',
                258: '8.9.11',
                259: '5.7.9.11.0',
                260: '1.2',
                261: '2.7.8',
                262: '3.8.9',
                263: '7.9.11.0',
                264: 'C#3',
                265: '0.2.4.7',
                266: '4.6.8.11',
                267: '4.9.10',
                268: '8.10.2',
                269: 'C6',
                270: '0.3',
                271: 'A3',
                272: 'C3',
                273: '3.5.7',
                274: '6.10',
                275: 'D7',
                276: '1.4.7',
                277: 'A6',
                278: '5.10',
                279: '4.6.10',
                280: '1.5.6.8',
                281: '9.10.0',
                282: 'E-5',
                283: '2.6.7',
                284: '9.11.3',
                285: '1.6',
                286: '9.0.2',
                287: 'F4',
                288: '0.4.8',
                289: '0.6',
                290: '9.0',
                291: 'E6',
                292: '5.7.9.0',
                293: '4.7.8.11',
                294: 'D3',
                295: '5.6.10.11',
                296: '11',
                297: '3.5.9',
                298: '4.7.10',
                299: '8.9.0.3',
                300: '1.4.8',
                301: '4.7.9.11.0',
                302: '4.8.11',
                303: 'E5',
                304: '6.7',
                305: '8.11',
                306: '5.7.10.0',
                307: '8.10.11',
                308: 'E1',
                309: '11.0.4.7',
                310: 'E4',
                311: '11.3.4',
                312: '8.9.0',
                313: '3.9',
                314: 'B5',
                315: '3.8',
                316: '7.11.0',
                317: '6.7.9',
                318: 'G#7',
                319: 'F#7',
                320: '10.11',
                321: '1.5.9',
                322: '6.8.10.2',
                323: 'B3',
                324: '10.11.3',
                325: '2.5.8',
                326: '3.7',
                327: '5.9.11',
                328: '6.7.0',
                329: '10.3.4',
                330: '10.0',
                331: '2.3.8',
                332: '8.1.2',
                333: '2.4',
                334: '5.8.10.0',
                335: '2.5.7.10',
                336: '5.11',
                337: '11.4',
                338: '10.3',
                339: '10',
                340: '4.7.11',
                341: '3.6.9.11',
                342: '2.5.8.10',
                343: '6.10.1',
                344: '2.6.7.9',
                345: 'F#2',
                346: '3.5.7.10',
                347: '5.6.10.1',
                348: 'C7',
                349: '2.4.8',
                350: '9.1.4.5',
                351: '0.2.3',
                352: '7.0.1',
                353: '6.8',
                354: '5',
                355: '5.8.0',
                356: 'G#5',
                357: 'G#6',
                358: '0.2.4.5.7',
                359: 'G#4',
                360: '1.4',
                361: '11.2.5.7',
                362: '3.5.8',
                363: '5.8.11',
                364: '10.0.2',
                365: '1.3',
                366: 'B-4',
                367: '9.0.2.5',
                368: '6.8.9',
                369: '5.7.9',
                370: '3.7.11',
                371: '2.3.7.10',
                372: '2.4.5.7.9.11',
                373: '0.2.7',
                374: '11.3.5.6',
                375: 'G3',
                376: '11.0.2.4.5.7',
                377: '11.1.5',
                378: '1.5.6',
                379: '9.11.0.2',
                380: '4.6.8',
                381: 'D4',
                382: '1.5.8',
                383: '9.11.2',
                384: '7.11.0.2',
                385: 'D2',
                386: '5.8',
                387: '4.6.9.11',
                388: '5.7.9.11',
                389: '3.4',
                390: 'E2',
                391: '2.4.5',
                392: 'B1',
                393: 'C#7',
                394: '7.9.11.2',
                395: 'F#3',
                396: '8.11.2.4',
                397: '1.7',
                398: '0.2.5.7',
                399: '4.5.9.0',
                400: 'F#1',
                401: 'G#1'}


@st.cache_resource
def load_model(model_file):
    model = tf.keras.models.load_model(model_file, compile=False)
    model.compile(loss="sparse_categorical_crossentropy", optimizer="adam")
    return model


def predict(model, input):
    prediction = model.predict(input)
    return prediction


def read_midi(file):

    print("Loading Music File:", file)

    notes = []
    notes_to_parse = None

    # parsing a midi file
    midi = converter.parse(file)

    # grouping based on different instruments
    s2 = instrument.partitionByInstrument(midi)

    # Looping over all the instruments
    for part in s2.parts:

        # select elements of only piano
        if 'Piano' in str(part):

            notes_to_parse = part.recurse()

            # finding whether a particular element is note or a chord
            for element in notes_to_parse:

                # note
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))

                # chord
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))

    return np.array(notes)


def convert_to_midi(prediction_output):

    offset = 0
    output_notes = []

    # create note and chord objects based on the values generated by the model
    for pattern in prediction_output:

        # pattern is a chord
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:

                cn = int(current_note)
                new_note = note.Note(cn)
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)

            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)

        # pattern is a note
        else:

            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)

        # increase offset each iteration so that notes do not stack
        offset += 0.5
    midi_stream = stream.Stream(output_notes)
    midi_stream.write('midi', fp='test_output.mid')


def convertToPrediction(file):
    with st.spinner(f"Transcribing to FluidSynth"):
        notes_array = read_midi(file)
        no_of_timesteps = 32
        x_test = []

        for i in range(0, len(notes_array) - no_of_timesteps, 1):
            # preparing input and output sequences
            input_ = notes_array[i:i + no_of_timesteps]

            x_test.append(input_)

        x_test = np.array(x_test)

        x_int_notes = []
        for sequence in x_test:
            int_sequence = [notes_in_int.get(note) for note in sequence]
            x_int_notes.append(int_sequence)

        x_int_notes = np.array(x_int_notes)

        # You can now use the 'no' list for your selected music
        selected_music_index = np.random.randint(0, len(x_int_notes) - 1)
        selected_music = x_int_notes[selected_music_index]

        # Generate variations or enhance the selected music
        variations = []
        for i in range(60):
            selected_music_reshaped = selected_music.reshape(
                1, no_of_timesteps)

            # Use the model to generate predictions or variations with temperature
            temperature = 0.5  # Adjust the temperature as needed
            prob = model.predict(selected_music_reshaped)[0]
            y_pred = np.random.choice(len(prob), p=prob)

            variations.append(y_pred)

            # Apply variations to the selected music
            selected_music = np.insert(
                selected_music, len(selected_music), y_pred)
            selected_music = selected_music[1:]

        variations_notes = [int_in_notes[i] for i in variations]

        convert_to_midi(variations_notes)
        midi_data = pretty_midi.PrettyMIDI('test_output.mid')
        os.unlink('test_output.mid')
        audio_data = midi_data.fluidsynth()
        audio_data = np.int16(
            audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
        )  # -- Normalize for 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.py

        virtualfile = io.BytesIO()
        wavfile.write(virtualfile, 44100, audio_data)

    st.audio(virtualfile)
    st.markdown("Download the audio by right-clicking on the media player")


notes_ = []
x_int_to_note = {number: note_ for number, note_ in enumerate(notes_)}
st.title("Mushit Generator")
model = load_model('model.h5')
file = st.file_uploader("Upload a midi", type="mid",
                        accept_multiple_files=False)
if file is not None:
    st.write("File uploaded")
    st.write("Generating music...")
    bytes_data = file.getvalue()
    # st.write(bytes_data)
    # stringio = io.StringIO(file.getvalue().decode("utf-8"))
    # st.write(stringio)
    # string_data = stringio.read()
    # st.write(string_data)

    convertToPrediction(bytes_data)
