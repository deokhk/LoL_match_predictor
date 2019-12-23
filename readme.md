# Team buidling Optimization in a Multi-player game
## 연구 목적
이번 연구의 주제는 Multi-player game 에서의 Team-building Optimization 이다. Multi-player video game 에서 유저는 특정 character 를 조작한다.

![](https://i.imgur.com/evp5YBz.jpg)
<center>[Fig 1 : Multi-player video game]</center>

보통 character 들은 각자 다른 능력치를 가지고 있으며, 유저의 퍼포먼스는 해당 character 를 어느 정도 잘 다루는지에 의해 결정된다. 유저의 캐릭터에 대한 숙련도가 다르고, 캐릭터 간에도 상성이 존재하기 때문에 어떠한 캐릭터를 플레이하느냐에 따라 유저의 승률은 크게 달라질 수 있다. 이 때 자신이 속한 팀원들의 퍼포먼스는 게임이 시작되기 전에 알 수 있지만, 상대 팀의 퍼포먼스는 알 수 없는 경우가 대부분이다.

그렇다면 이러한 제한된 정보 상황에서 유저는 게임에서의 승률을 높이기 위해 어떠한 캐릭터를 플레이해야 될까?

**이번 연구에서는 이러한 제한된 정보 상황에서 3 가지의 team building 방법론을 제시하고, 이를 league of legends game data 에 적용하여 평가해 보았다.**
## 연구 배경
 Team-building 은 고전적이지만 많은 영역에 적용되고 있는 문제이다. 스포츠 경기와 조별 과제 등 일상 생활에 맞닿아 있는 부분부터 시작하여, 군사 작전과 동맹 관계등 국가의 운명을 건 문제에 이르기까지, 집단 간의 협력이 요구되는 분야에 빠질 수 없는 것이 Team building 이다.
 
 우리가 일상 생활에서 주로 마주하는 Team-building 의 경우 군사 작전등 중대한 문제에 관한 Team-building 이라기 보다는 스포츠 경기와 같은 여가 활동에 수반하는 Team-building 이다. 따라서 이번 연구에서는 스포츠 경기, 그 중에서도 Esports 에 집중하여 연구를 수행해 나가고자 한다. 다양한 E-sports 중 “League of Legends” 을 대상으로 연구를 진행할 것이다.
  
 Leagueof Legends(LOL)은 1억명 이상의 MAU를 보유하고 있는 AOS게임이다.
LOL 에서는 두 팀(red, blue)이 한 경기의 승리를 향해 다투며, 각 팀은 5 명의 플레이어로 구성된다. 이때 팀은 각각 탑, 미드, 정글, 원딜, 서폿의 5 가지 역할군의 조합으로 구성되며, 플레이어는 역할군 중 하나를 다른 팀원과 중복없이 선택한 후, 역할군을 수행하기 적합한 챔피언(character)를 골라 플레이한다.

 League of legends 의 대표적인 map 인 소환사의 협곡에는 3 가지의 라인(전장)이 있다. 탑, 미드, 바텀이 그것이다. 원딜 역할군과 서폿 역할군은 함께 바텀라인에서 플레이하게 되며, 원딜과 서폿의 조합을 “바텀 듀오"라고 한다.
 <center><img src="https://i.imgur.com/mJQjIn5.jpg" ></center>
 
<center>[Fig 2 : Summoner's Lift Map]</center>

 **이번 연구에서는 이 중 상대 바텀 듀오가 주어졌을때, 최고의 승률을 내기 위해서는 어떠한 바텀 듀오를 구성해야 되는지를 추천하는 모델에 대해 다루고자 한다.**
## 연구 방법
연구는 크게 3 단계로 이루어진다. 데이터수집, 모델 학습, 평가 순서로 이루어진다.
1. 데이터 수집
    ![](https://i.imgur.com/Bqsw4vY.png)
    
    League of Legends는 게임의 전적을 수집할 수 있는 API를 제공한다. 위와 같은 방법으로 해당 API를 이용하여 매치 정보를 수집하기 위한 Python Script 를 작성하였다. 총 32000 개의 Match Data 를 수집하였다.
    
    ![](https://i.imgur.com/HcZSqbV.jpg)
    <center>[Fig 3. Match Data Crawler written in Python]</center>
    이후 뉴럴 네트워크 모델에 필요한 데이터를 기준으로 Parsing 하고 재구성하였으며, 재구성한 내용을 csv 파일 형태로 저장하여 NN 을 training 할 때 input 과 label 로 사용할 수 있도록 하였다.
2. Keras를 이용한 뉴럴 네트워크 모델 생성 및 학습
    Google Colab 상에서 Keras 를 이용하여 뉴럴 네트워크 모델을 생성하고, 학습시켰다. **총 3 개의 binary classifer model (simple model, complex model, final model)과 1 개의 linear regression model (performance model)을 구현하였고 학습시켰다.** 각 모델의 뉴럴 네트워크 구조는 모두 동일하다. Input layer 와 하나의 fully-connected hidden layer(relu), output layer(sigmoid, performance model 인 경우는 g(z) = z)로 구성되어있다.
    * simle model (binary classifier)
simple model 은 **각 바텀 듀오가 선택한 챔피언 정보만을 input 으로 제공하였다.**

        (# of input feature = 4 , # of training data = 26000, # of validation data = 6409) / label = win-lose info of red team)
    * complex model (binary classifier)
simple model 의 input 에 더하여 **바텀듀오 한 팀의 게임 내에서의 stat 정보(kill, assist, damage 등)를 추가로 input 으로 제공**하였다.

        (# of input feature = 114 , # of training data = 52000, # of validation data = 12818) / label = win-lose info of red team)
    *  final model (binary classifier)
simple model 의 input 에 더하여, **팀 내 각 player 들의 performance score 를 추가로 input 으로 제공**한다.

        **Performance score** 는 해당 유저의 게임 내에서의 stat 정보를 바탕으로 계산되는 유저의 실력 수치이며, performance model 의 return 값이다.
        해당 수치는 0과 2 사이의 실수이다. **0은 플레이어의 stat 정보를 바탕으로 평가해 보았을 때, 플레이어는 플레이어가 속한 유저군 사이에서 게임을 하였을 때 0% 승률 만큼의 실력을 가지고 있음을 의미하고. 1 은 50%, 2 는 100%를 의미한다.**

        (# of input feature = 14 , # of training data = 26000, # of validation data = 6409) / label = win-lose info of red team)
    * performance model (linear regression)
**performance model 은 유저의 게임 내에서의 stat 정보를 input 으로 받아, 유저의 performance score(0~2 사이)를 리턴**한다.

        Match data crawler 는 특정 유저의 encrypted-id 를 주고 해당 유저가 플레이한 최근 100 개의 게임을 리턴하는 riot api 를 활용하여 match data 를 수집한다. 이렇게 리턴되는 100 개의 match 에 대해, 각 match 에서 특정 유저가 어떠한 챔피언을 플레이하였는지 기입하고 해당 match 에서의 stat, 승패여부를 저장하였다. 해당 정보는 championid 를 key 값으로 가지는 dictionary 에 저장된다.

        **한 플레이어가 플레이한 최근 100 개의 게임을 모두 처리한 뒤, 해당 구간 동안 플레이어가 5 경기 이상 플레이 한 챔피언들을 대상**으로,
        input: "챔피언 정보" + "해당 챔피언을 플레이한 경기들에서 얻은 stat 값의 평균"와 label: "해당 챔피언을 플레이 하였을 때의 승률“을 추출하여 학습시켰다.
        
        (# of input feature = 57, # of training data = 1130, # of test data = 285)
## 연구 결과 및 평가
수집된 match data 를 8:2 로 나눠 80%는 train data 로, 20%는 validation data 로 사용하였다. binary classifier 인 simple,complex,final model 에서의 **accuracy 는 주어진 데이터를 바탕으로 model 이 예측한 승리 여부와 실제 label 의 값을 비교함으로서 계산된다.**

세 모델 모두 adam optimizer 를 사용하였다. 또한 loss function 으로는 “binary closs entropy loss”를 도입하여 사용하였다.

![](https://i.imgur.com/iiDxyZE.jpg)
<center>[Fig 4. Binary closs entropy loss]</center><br>

### Simple Model
<center><img src = "https://i.imgur.com/uM7VjJH.jpg" width = "700" ></center>

<center>[Fig 5. Simple Model]</center><br>

 Simple model 의 경우 학습이 진행됨에 따라 train data 와 validation data 의 loss 가 감소하는 것을 확인할 수 있으나, 10 번째 iteration 이후로부터는 변화가 거의 없는 것을 확인할 수 있다. 또한, train data 에서의 accuracy 와 validation data에서의 accuracy 는 50%를 중심으로 진동하는 것을 확인할 수 있다.
 
 **아마 input feature 의 수가 학습하기에는 너무 적은 숫자이거나, 혹은 input feature 로 준 두 팀의 바텀 듀오의 조합이 게임의 승리에 크게 영향을 미치지 않는다는 것으로도 해석할 수 있다.**
 
### Complex Model
<center><img src = "https://i.imgur.com/T9qfyqs.jpg" width = "700" ></center>

<center>[Fig 6. Complex Model]</center><br>

complex model 의 경우도 마찬가지로 50% 정도의 accuracy 를 보여준다. simple model 과 유사한 데이터가 관찰되는 것을 확인 할 수 있다.<br>**simple model 과 complex model 의 결과를 통해 바텀 듀오의 조합과 두 팀의 바텀 듀오 중 한팀의 바텀 듀오의 stat 만으로 게임의 결과를 예측하기는 힘들다는 것을 확인할 수 있다.**
### Final Model

<center><img src = "https://i.imgur.com/gwibrJO.jpg" width = "700" ></center>

<center>[Fig 7. Final Model]</center><br>

다만 게임에 참여한 10 명 모두의 performance score 를 계산하고 이를 바텀 듀오의 조합과 더불어 input feature 로 제공한 final model 에서는, simple model 과 complex model 과 다르게 68% 정도의 accuracy 를 얻을 수 있었다. 

**이를 통해 게임에 참여하는 10 명의 performance score 가 게임의 승부를 결정짓는데 중요한 역할을 한다는 것을 확인할 수 있었다.**

**현재 performance score 를 예측하는 performance model 은 높은 정확성을 가지고 작동하지 않는다.** 데이터의 개수가 너무 부족하기 때문이다. LOL 에서 제공하는 riot api 에는 call rate limit 이 존재한다. 따라서 1.3 초당 하나의 match data 를 얻을 수 있으며 24 시간이 지나면 api key 가 파기되어 연속적인 수집을 불가능하게 한다. 게다가 수집한 match data 중 bottom duo를 알아내기 어려운 case 가 전체의 1/3 정도이고, 나머지 2/3 도 수집하고자 하는 기간에 해당하지 않는 매치인 경우가 절반 이상이다.

이에 더해 performance model 의 input data 는 더 많은 제약조건을 걸고 데이터를 수집한 match data 들의 평균치이기 때문에, 기본적으로 data 를 많이 수집하기가 어렵다. 그럼에도 불구하고 성능의 향상을 보여준 것은, 고무적이다.
<center><img src = "https://i.imgur.com/DyEPjxS.jpg" width = "550" ></center>

<center>[Fig 8. Performance Model]</center><br>

Fig 8 은 학습이 진행됨에 따라 Mean absolute Error 의 변화를 나타낸 것이다. 500 번의 Iteration 뒤에는 Train Error/Var Error 모두 더 이상 감소하지 않는 것을 확인할 수 있다.

## 토론 및 전망
연구의 최종 목표는 상대 바텀 듀오가 주어졌을때, 최고의 승률을 내기 위해서는 어떠한
바텀 듀오를 구성해야 되는지를 예측하는 모델을 만드는 것이다.

이는 Final Model 에 자신의 바텀 듀오를 제외한 다른 모든 플레이어들의 performance score 를 1 로 주고(50%의 승률을 가지고 있다고 가정) 나머지 parameter(자신의 바텀 듀오의 champion, 해당 champion 에 대해 측정된 performance score)를 변화시키면서 1 에 가장 가까운 예측값을 산출하는 bottom duo champion 을 추천하면 될 것이다.
[](https://)
68% Accuracy 는 아직 많이 부족한 수치이다. 이를 높이기 위하여 우선 Performance model 을 개선시키고자 한다. Performance model 에 제공되는 학습 데이터의 수를 늘려 유저의 Performance Score 예측을 보다 정확하게 하고자 한다.