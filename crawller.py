import requests
import csv
import json
from ratelimiter import RateLimiter


PAGE_END = 34

rate_limiter = RateLimiter(max_calls=3, period=4)
f = open('simple_model_data.csv', 'w', encoding='utf-8', newline='')
lf = open('simple_model_label.csv', 'w', encoding='utf-8', newline='')

df = open('complex_model_data.csv', 'w', encoding='utf-8', newline='')
ldf =open('complex_model_label.csv', 'w', encoding='utf-8', newline='')

sf = open('standard_performance_data.csv', 'w', encoding='utf-8', newline='')
lsf = open('standard_performance_label.csv', 'w', encoding='utf-8', newline='')

ff = open('final_model_data.csv', 'w', encoding='utf-8', newline='') #simple model과 같이 사용되어야 함.
lff = open('final_model_label.csv', 'w', encoding='utf-8', newline='')


simple_model_data_wr = csv.writer(f)
simple_model_label_wr = csv.writer(lf)

complex_model_data_wr = csv.writer(df)
complex_model_label_wr = csv.writer(ldf)

standard_performance_data_wr = csv.writer(sf)
standard_performance_label_wr = csv.writer(lsf)

final_model_data_wr = csv.writer(ff)
final_model_label_wr = csv.writer(lff)



api_list = []
api_list.append('')
api_list.append('')
api_list.append('')

#Get summoner name of DIAMOND 1 USERS

summoner_namelist=[]
summoner_accountid=[]
pagenum=1

while len(summoner_namelist) < 3000:
    with rate_limiter:
        API_KEY=''
        url = 'https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?page='+str(pagenum)+'&api_key='+API_KEY
        data = requests.get(url).json()
        for i in range(len(data)):
            if 'summonerName' in data[i]:
                a_summoner_name = data[i]['summonerName']
                summoner_namelist.append(a_summoner_name)
        pagenum=pagenum+1

print(summoner_namelist)

api_key_number = len(api_list)

summoner_findlist=[]
#Get encrypted summoner id of DIAMOND 1 USERS
for i in range(len(summoner_namelist)):
    with rate_limiter:
        if api_key_number * i +api_key_number>= len(summoner_namelist):
            break
        for a in range(len(api_list)):
            API_KEY=api_list[a]
            url='https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/'+str(summoner_namelist[api_key_number*i+a])+'?api_key='+API_KEY
            data=requests.get(url).json()
            if 'accountId' in data:
                summoner_accountid.append(data['accountId'])
                summoner_findlist.append(summoner_namelist[api_key_number*i+a])
                print("Encrypted id added" + str(api_key_number*i+a))


#Get match id of all users

match_id_list=[]

delimiter_number=100
summoner_added_sequence=[]

for i in range(len(summoner_accountid)):
    with rate_limiter:
        if api_key_number * i +api_key_number>= len(summoner_accountid):
            break
        for a in range(len(api_list)):
            API_KEY=api_list[a]
            url= 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/'+str(summoner_accountid[api_key_number*i+a])+'?queue=420&season=13&api_key='+API_KEY
            data = requests.get(url).json()
            single_player_match_id=[]
            if 'matches' in data:
                summoner_added_sequence.append(summoner_findlist[api_key_number * i + a])
                for j in range(len(data['matches'])):
                    if 'gameId' in data['matches'][j]:
                        single_player_match_id.append(data['matches'][j]['gameId'])
                        print("match of a user added : " + str(data['matches'][j]['gameId']))
                single_player_match_id.append(delimiter_number)
                delimiter_number=delimiter_number+100
            match_id_list = match_id_list + single_player_match_id

#Get match datas of collected match ids

summoner_idx=0
target_summoner = summoner_added_sequence[0]
one_person_match_info = {}

total_match_with_target_player = 0
found_match_with_target_player=0


for i in range(len(match_id_list)):
    with rate_limiter:
        if api_key_number * i +api_key_number>= len(match_id_list):
            break
        for a in range(len(api_list)):
            API_KEY=api_list[a]
            if int(match_id_list[api_key_number*i+a])<1000000:
                print("now entering..")
                print(one_person_match_info)
                summoner_idx=summoner_idx+1
                target_summoner=summoner_added_sequence[summoner_idx]
                champion_keyset = list(one_person_match_info.keys())
                for key in champion_keyset:
                    total_match_num = one_person_match_info[key]['win'] + one_person_match_info[key]['lose']
                    if total_match_num<5:
                        continue
                    print("total number of match on this champion" + str(total_match_num))
                    performance_data = []
                    performance_data.append(one_person_match_info[key]['champ'])

                    single_stat_len = len(one_person_match_info[key]['stat'][0])
                    averaged_data=[0 for x in range(single_stat_len)]


                    for stat_num in range(total_match_num):
                        print("Number of elements" + str(len(one_person_match_info[key]['stat'][stat_num])))


                    for stat_num in range(total_match_num):
                        arr = one_person_match_info[key]['stat'][stat_num]
                        print("Number of elements--" + str(len(one_person_match_info[key]['stat'][stat_num])))
                        print(arr)
                        for single_stat_num in range(single_stat_len):
                            averaged_data[single_stat_num]=averaged_data[single_stat_num]+arr[single_stat_num]

                    for single_stat_num in range(single_stat_len):
                        averaged_data[single_stat_num]=averaged_data[single_stat_num]/single_stat_len

                    performance_data=performance_data+averaged_data
                    standard_performance_data_wr.writerow(performance_data)

                    performance_label=[]
                    performance_label.append(2 * one_person_match_info[key]['winrate'])
                    standard_performance_label_wr.writerow(performance_label)


                one_person_match_info={}
                print("total match : " + str(total_match_with_target_player) + "found match : " + str(found_match_with_target_player))
                total_match_with_target_player = 0
                found_match_with_target_player = 0

                continue

            url='https://kr.api.riotgames.com/lol/match/v4/matches/'+str(match_id_list[api_key_number*i+a])+'?api_key='+API_KEY
            data=requests.get(url).json()
            if 'participants' not in  data:
                print("participants not in data")
                continue
            if 'gameVersion' in data:
                if data['queueId']!=420:
                    print("this is not ranked game") # TODO: add version
                    #jump to the another people's league of legends matchs
                    # temp = api_key_number * i
                    # while int(match_id_list[temp])>=1000000:
                    #     temp=temp+1
                    # i = int(temp/api_key_number)-1
                    continue

            bot_duo_team1_list=[]
            bot_duo_team2_list=[]
            participants = data['participants']

            for j in range(len(participants)):
                if 'teamId' in participants[j] and participants[j]['teamId']==100 and participants[j]['timeline']['lane'] == "BOTTOM":
                    bot_duo_team1_list.append(j)
                elif 'teamId' in participants[j] and participants[j]['timeline']['lane'] == "BOTTOM":
                    bot_duo_team2_list.append(j)

            if len(bot_duo_team1_list)!=2 or len(bot_duo_team2_list)!=2:
                continue

            team1_win=0
            team2_win=0
            if data['teams'][0]['win']=='Win':
                team1_win=1
            else:
                team2_win=1

            bot_duo_match_info =[] #0 -> team1_ad, 1 ->team1_sup, 2->team2_ad, 3->team2_sup

            is__team1_carry = participants[bot_duo_team1_list[0]]["stats"]["totalMinionsKilled"] > participants[bot_duo_team1_list[1]]["stats"]["totalMinionsKilled"]

            if is__team1_carry:
                bot_duo_match_info.append(participants[bot_duo_team1_list[0]]['championId'])
                bot_duo_match_info.append(participants[bot_duo_team1_list[1]]['championId'])
            else:
                bot_duo_match_info.append(participants[bot_duo_team1_list[1]]['championId'])
                bot_duo_match_info.append(participants[bot_duo_team1_list[0]]['championId'])

            is__team2_carry = participants[bot_duo_team2_list[0]]["stats"]["totalMinionsKilled"] > participants[bot_duo_team2_list[1]]["stats"]["totalMinionsKilled"]

            if is__team2_carry:
                bot_duo_match_info.append(participants[bot_duo_team2_list[0]]['championId'])
                bot_duo_match_info.append(participants[bot_duo_team2_list[1]]['championId'])
            else:
                bot_duo_match_info.append(participants[bot_duo_team2_list[1]]['championId'])
                bot_duo_match_info.append(participants[bot_duo_team2_list[0]]['championId'])

            simple_model_data_wr.writerow(bot_duo_match_info)

            bot_duo_match_info_label=[]
            bot_duo_match_info_label.append(team1_win)

            simple_model_label_wr.writerow(bot_duo_match_info_label)
            final_model_label_wr.writerow(bot_duo_match_info_label)

            print(bot_duo_match_info)
            print(match_id_list[api_key_number*i+a])

            bot_duo_index_info = bot_duo_team1_list + bot_duo_team2_list

            statstic_keyset=["firstBloodAssist","visionScore","magicDamageDealtToChampions","damageDealtToObjectives","totalTimeCrowdControlDealt","longestTimeSpentLiving",
                             "tripleKills","kills", "neutralMinionsKilled", "damageDealtToTurrets", "physicalDamageDealtToChampions",
                             "largestMultiKill", "totalUnitsHealed", "wardsKilled", "largestCriticalStrike", "largestKillingSpree", "quadraKills", "teamObjective", "magicDamageDealt",
                             "neutralMinionsKilledTeamJungle", "damageSelfMitigated","magicalDamageTaken","firstInhibitorKill","trueDamageTaken","assists","combatPlayerScore",
                             "goldSpent","trueDamageDealt","totalDamageTaken","physicalDamageDealt","sightWardsBoughtInGame","totalDamageDealtToChampions","physicalDamageTaken","totalPlayerScore",
                             "objectivePlayerScore","totalDamageDealt","neutralMinionsKilledEnemyJungle","deaths","wardsPlaced","turretKills","firstBloodKill","trueDamageDealtToChampions","goldEarned",
                             "killingSprees","unrealKills","firstTowerAssist","firstTowerKill","champLevel","doubleKills","inhibitorKills","firstInhibitorAssist",
                             "visionWardsBoughtInGame","pentaKills","totalHeal","totalMinionsKilled","timeCCingOthers"]

            #Gather data for team 1
            single_match_info = []
            for j in range(len(bot_duo_index_info)):
                idx = bot_duo_index_info[j]
                single_player_info = []
                single_player_info.append(participants[idx]['championId'])
                if j>=2:
                    continue
                for k in statstic_keyset:
                    single_stat = participants[idx]['stats'].get(k)
                    if single_stat is None:
                        single_stat=0
                    if isinstance(single_stat, bool):
                        single_stat = int(single_stat == 'true')
                    single_player_info.append(single_stat)
                single_match_info=single_match_info+single_player_info

            complex_model_data_wr.writerow(single_match_info)

            single_match_info_label = []
            single_match_info_label.append(team1_win)

            complex_model_label_wr.writerow(single_match_info_label)

            #Gather data for team2
            single_match_info = []

            front=bot_duo_index_info[0:2]
            end=bot_duo_index_info[2:4]

            bot_duo_match_info=end+front


            for j in range(len(bot_duo_index_info)):
                idx = bot_duo_index_info[j]
                single_player_info = []
                single_player_info.append(participants[idx]['championId'])
                if j>=2:
                    continue
                for k in statstic_keyset:
                    single_stat = participants[idx]['stats'].get(k)
                    if single_stat is None:
                        single_stat=0
                    if isinstance(single_stat, bool):
                        single_stat = int(single_stat == 'true')
                    single_player_info.append(single_stat)
                single_match_info=single_match_info+single_player_info

            complex_model_data_wr.writerow(single_match_info)

            single_match_info_label = []
            single_match_info_label.append(team2_win)

            complex_model_label_wr.writerow(single_match_info_label)



            player_name_list=[]
            for j in range(len(participants)):
                current_player_name = data['participantIdentities'][j]['player']['summonerName']
                player_name_list.append(current_player_name)

            total_match_with_target_player=total_match_with_target_player+1
            print("We are looking for target summoner:" + target_summoner)
            for j in range(len(player_name_list)):
                player_account_name = player_name_list[j]

                if target_summoner==player_account_name:
                    found_match_with_target_player=found_match_with_target_player+1
                    print("we found the targer player")
                    select_champion = participants[j]['championId']
                    is_player_win = 0
                    if participants[j]['teamId'] == 100 and team1_win == 1:
                        is_player_win = 1
                    elif participants[j]['teamId'] == 200 and team2_win == 1:
                        is_player_win = 1

                    if select_champion in one_person_match_info:
                        player_champion_info = one_person_match_info[select_champion]
                        win_info = player_champion_info['win'] + int(is_player_win == 1)
                        lose_info = player_champion_info['lose'] + int(is_player_win == 0)
                        win_rate = win_info / (win_info + lose_info)
                        champion_stats = player_champion_info['stat']
                        single_player_stat_data = []
                        for k in statstic_keyset:
                            single_stat = participants[j]['stats'].get(k)
                            if single_stat is None:
                                single_stat = 0
                            if isinstance(single_stat, bool):
                                single_stat = int(single_stat == 'true')
                            single_player_stat_data.append(single_stat)
                        champion_stats.append(single_player_stat_data)
                        player_champion_info['win'] = win_info
                        player_champion_info['lose'] = lose_info
                        player_champion_info['stat'] = champion_stats
                        player_champion_info['winrate'] = win_rate
                    else:
                        player_champion_info = {}
                        win_info = int(is_player_win == 1)
                        lose_info = int(is_player_win == 0)
                        win_rate = win_info / (win_info + lose_info)
                        initial_stat_data=[]
                        single_player_stat_data = []
                        for k in statstic_keyset:
                            single_stat = participants[j]['stats'].get(k)
                            if single_stat is None:
                                single_stat = 0
                            if isinstance(single_stat, bool):
                                single_stat = int(single_stat == 'true')
                            single_player_stat_data.append(single_stat)
                        initial_stat_data.append(single_player_stat_data)
                        player_champion_info['win'] = win_info
                        player_champion_info['lose'] = lose_info
                        player_champion_info['stat'] = initial_stat_data
                        player_champion_info['champ'] = select_champion
                        player_champion_info['winrate'] = win_rate
                        one_person_match_info[select_champion] = player_champion_info
            print("===========================")


            final_model_player_index=front+end

            for j in range(len(participants)):
                if j in final_model_player_index:
                    continue
                final_model_player_index.append(j)


            single_match_info = []

            for idx in final_model_player_index:
                single_player_info = []
                single_player_info.append(participants[idx]['championId'])
                for k in statstic_keyset:
                    single_stat = participants[idx]['stats'].get(k)
                    if single_stat is None:
                        single_stat=0
                    if isinstance(single_stat, bool):
                        single_stat = int(single_stat == 'true')
                    single_player_info.append(single_stat)
                single_match_info=single_match_info+single_player_info

            final_model_data_wr.writerow(single_match_info)


f.close()
df.close()
lf.close()
ldf.close()
sf.close()
lsf.close()
ff.close()
lff.close()

print("We are done!")

