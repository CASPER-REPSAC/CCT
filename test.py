list = """
9	17
1a1b	13.5	25
aaa7117	9.5	17
abc1234	10	18
abcd13	4.5	8
aim3636	14.5	27
am1029	4	7
babo04	17.5	32
baekho	16	29
bin1017	19	35
break03	11	20
case	5	9
chiara	13.5	25
cowe97	17.5	32
dani22	0	0
deku77	15	28
dodo12	13.5	25
exu37	11	20
gamja13	15.5	29
green5	13.5	25
gyung07	11.5	21
ham999	16	29
hanyul04	7	13
hatemath	6.5	12
hka	10	18
hos	12.5	23
hr0710	11.5	21
hsk27	13	24
jjjj53	16	29
k00098	8	15
keras21	10.5	19
lak4021	13	24
leesan6	10.5	19
leona16	12.5	23
lilili	11	20
lily	14.5	27
lsp	5	9
mathking	0	0
mello47	16	29
mhd1229	5	9
mrchar	10.5	19
mugeun1	7.5	14
notjsj	15	28
notporq	17	31
orange1	10.5	19
owl321	9	17
pengpeng	16	29
ponch12	17	31
qaeawa	17	31
qood123	16.5	30
qwer1234	10.5	19
song20	8	15
sp2077	16.5	30
summer04	18	33
thisis1	7	13
wsxuj	0	0
yamtu1u	8.5	16
zizon17	7	13
zz67	12	22
zzzzz11	0	0
"""

list = list.split()
result = 0
print(list)
for i in range(len(list)):
    if i % 3 == 1 :
        print(list[i])
        result += float(list[i])
        
print('aver: ', result/51)