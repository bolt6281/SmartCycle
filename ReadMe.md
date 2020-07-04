<center>

<img src="C:\Users\bolt6281\Desktop\SmartCycle_logo_skyblue.png" alt="SmartCycle_logo_skyblue" style="zoom:25%;" />



<h2 align="center"><b>SmartCycle</b></h2>

<h4 align="center">Sort up Trash by Oneshot</h4>

​														<center>[<img src="https://camo.githubusercontent.com/e23adf1955ff7979d1ea24029a1f11b485011d27/68747470733a2f2f6c68332e676f6f676c6575736572636f6e74656e742e636f6d2f636a73717257514b4a51703952464f372d684a394166704b7a6255625f5938347658666a6c503069524842766c61647741665869683938346f6c6b744468506e4671795a306e753941356a7646774f455150587a76376872336365335156734c4e386b5132416f3d7330" alt="img"  />](https://play.google.com/store/apps/details?id=com.dimipo.smartcycle)</center>



## Introduction

모두를 위한 인공지능 분리수거 도우미 SmartCycle은 카메라 앞에 쓰레기를 보여주며 어떻게 버리는 지 물어보면 음성으로 사용자의 분리수거를 도와주는 서비스입니다. 

핵심 기능 이외에도 분리수거 퀴즈를 제공하며, 모바일 앱으로도 SmartCycle을 이용할 수 있습니다. 모바일 앱에서는 촬영을 통한 쓰레기 검색, 쓰레기 관련 게시글 조회, 수동 검색 등을 지원하고 있습니다(모바일에서는 이미지와 텍스트를 통해 분리수거 방법을 안내합니다).

모바일 앱에 관한 더 자세한 내용은 [여기](https://github.com/MODORIAPPS/SmartCycle-Sort_up_Trash_by_Oneshot)를 참고해주세요.
서버에 관한 내용은 [여기](https://github.com/whoisStarBox/SmartCycle_server)를 참고해주세요.



## SmartCycle(Raspberry Pi)

이 부분은 스마트사이클 기기에 탑재되는 라즈베리파이에서 작동하는 시스템입니다.



인공지능 스피커 NUGU가 서버에 촬영을 요청하는 신호를 보내면 스마트사이클이 서버로부터 신호를 받고
이미지를 촬영 후 해당 스마트사이클의 고유번호와 함께 이미지를 서버로 전송합니다.



- main.py : websocket을 통한 서버와의 통신, 이미지 촬영, QR code 인식 등을 진행하는 메인 프로그램

- post.py : 서버에 데이터를 전송하는 모듈



## SmartCycle_AI(Server)

SmartCycle의 데이터 수집/데이터 증대/모델 학습 및 서버에서 작동하는 쓰레기 인식 시스템에 대한 부분입니다.



분류하는 쓰레기의 종류는 배터리, 부탄가스, 종이팩, 유리병, 내열유리, 페트병, 약통, 스티로폼, 휴지, 우산으로 총
10가지입니다. 더 많은 종류를 학습시키고 싶었지만 촬영에 필요한 물품을 준비하는데 어려움과 많은 시간이 소요될 것으로 예상되어 일상생활에서 가장 많이 사용하지만 가장 많이 실수하는 10가지를 선정하였습니다.

ex) 내열유리 : 유리가 아닌 일반 쓰레기에 버려야 함 / 부탄가스 : 구멍을 뚫고 내용물을 모두 제거한 뒤 버려야 함



#### 데이터 수집(SmartCycle_DataCollector)

다양한 쓰레기의 이미지 데이터셋을 구할 수가 없었기 때문에 직접 데이터셋을 제작하기로 결정했습니다.

2000장(한 class 당 200장)의 이미지를 촬영하였습니다. 절반씩은 각각 밝은 곳과 어두운 곳에서 촬영하였습니다.

- SmartCycle_DataCollector.py : 키를 누를 때마다 촬영하고 있는 이미지를 원하는 위치에 저장

- save_img.py : 지정한 size, 위치, 이름으로 이미지를 저장하는 모듈



#### 데이터 예시

<img src="C:\Users\bolt6281\programming\Python\Team Projects\2019 STAC\data\dataset\train\image-57.jpg" alt="image-57" style="zoom:33%;" /><img src="C:\Users\bolt6281\programming\Python\Team Projects\2019 STAC\ObjectDetection\test1.jpg" alt="test1" style="zoom:33%;" /><img src="C:\Users\bolt6281\programming\Python\Team Projects\2019 STAC\data\raw_data\glass_bottle_2\image8.jpg" alt="image8" style="zoom:33%;" />

<img src="C:\Users\bolt6281\programming\Python\Team Projects\2019 STAC\data\raw_data\heat_resistant_glass_1\image43.jpg" alt="image43" style="zoom: 33%;" /><img src="C:\Users\bolt6281\programming\Python\Team Projects\2019 STAC\data\raw_data\pet_1\image160.jpg" alt="image160" style="zoom:33%;" /><img src="C:\Users\bolt6281\programming\Python\Team Projects\2019 STAC\data\raw_data\tissue_2\image24.jpg" alt="image24" style="zoom:33%;" />



* 라벨링은 [labelImg](https://github.com/tzutalin/labelImg)를 이용하였습니다.

#### 데이터 증대(data aumentation)

부족한 데이터를 보완하고자 다양한 상황에서 높은 인식률을 가질 수 있도록 좌우반전(Vertical Flip Augmentation), 0~30도 사이의 무작위 각도 회전(Rotation Augmentation), 밝기 조절(Brightness Augmentation) 기법을 이용하여 데이터셋을 4배 이상 부풀렸습니다.

- data_augmentation.py : 폴더 내의 이미지에 회전, 밝기, 좌우반전을 통해 데이터를 증대하고 저장

- suffle&save.py : 모든 데이터를 무작위로 섞고 파일명을 변경하여 한 폴더에 저장

  데이터를 순서대로 학습시키면 학습이 원활하게 진행되지 않을 확률이 높기에 class별로 나누어져있던 파일들의 파일명을 랜덤으로 변경하였습니다.



#### 모델 선정 이유와 학습(SmartCycle_Trainer, 용량 문제로 미첨부)

- Object Detection 

  부족한 데이터를 보완하기 위해 [Tensorflow Object Detection API](https://github.com/tensorflow/models)의 Pre-trained 모델을 이용하기로 결정했고, 서버 환경이 Object Detection 모델을 작동시키기에 원활하지 않지만 높은 정확도를 최우선으로 하여  [Faster R-CNN Inception v2 coco](http://download.tensorflow.org/models/object_detection/faster_rcnn_inception_v2_coco_2018_01_28.tar.gz) 모델을 선정하였습니다.  공모전 종료 며칠 전에 학습을 시작해서 Yolo 모델 학습은 시도해보지 못했지만, 데이터만 충분하다면 Yolo모델이 빠른 처리가 요구되는 SmartCycle에 더욱 적합할 것입니다.

  [How to train an Object Detector using Tensorflow API on Ubuntu 16.04 (GPU)](https://github.com/Khaivdo/How-to-train-an-Object-Detector-using-Tensorflow-API-on-Ubuntu-16.04-GPU) 참고

  

학습이 고성능의 컴퓨팅 파워를 요구하였기 때문에 실제 학습은 Google Cloud Platform에서 제공하는 Vm instance(V100 16GB 1개)에서 진행하였습니다.



ObjectDetection 폴더에서 다음과 같이 환경변수를 설정하고 webcam.py를 실행하여 모델의 성능을 테스트해볼 수 있습니다(CPU).

```command
set PYTHONPATH= .\models;.\models\research;.\models\research\slim
python webcam.py
```

- frozen_inference_graph.pb : 학습된 모델 파일

- classifier(run by js).py : 서버에서  0.1초 간격으로 특정 폴더를 확인하고, 파일이 생겼을 때 모델을 이용하여 예측(Predict)하고 결과값을 출력함.

서버에서는 이 프로그램이 출력하는 결과를 받아 쓰레기 분리수거 정보 데이터베이스에서 해당 쓰레기의 분리수거 방법을 조회하고, 안내 메시지를 인공지능 스피커(NUGU)에게 전송하면 스피커는 사용자가 들고있는 쓰레기의 분리수거 방법을 안내합니다.



## License

SmartCycle_AI/SmartCycle_Trainer/ObjectDetection/models는 Apache License 2.0을 따르며 
이 외의 코드는 참고하셔도 좋습니다.

궁금한 점이 있거나 SmartCycle_Trainer(모델과 classifier) 또는 본 프로젝트에 쓰인 데이터셋을 필요로 하신다면 간단한 이유와 함께
bolt6281@gmail.com으로 연락부탁드립니다. 피드백도 주시면 감사하겠습니다.

