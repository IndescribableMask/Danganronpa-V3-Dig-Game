# Danganronpa-V3-Dig-Game
Danganronpa V3 Dig Game [Rank S] Solution

### Prepare
`python3.7`
`numpy`
`cv2`

### Introduction
This code is for DanganranpoV3 dig game rank S solution.

You need to take a screenshot of the game interface and rename it first. 

`/1.png  # this is your screenshot file, named "1.png".`

The code will automatically recognize the colors of the blocks in the screenshot and convert them into np.array. 

Then, the code will simulate the elimination situation automatically. 

It will record the final remaining blocks number and the whole steps , of the optimal solution. 

You just need to follow the elimination prompts step by step after the simulation is completed. 

Press Enter to get the next step.

The code does not guarantee success in one attempt, but it will succeed after multiple tries.

### Run
`python3 dig_game.py`

### Examples
screenshot example
![1](https://github.com/IndescribableMask/Danganronpa-V3-Dig-Game/assets/38174687/b34d9b81-9fb4-4ade-9ac7-8f92cf63d5a7)

simulate example
![微信截图_20230923105214](https://github.com/IndescribableMask/Danganronpa-V3-Dig-Game/assets/38174687/18929db2-ac6a-46bb-9a7d-426abc99e84b)
![微信截图_20230923105721](https://github.com/IndescribableMask/Danganronpa-V3-Dig-Game/assets/38174687/f973700a-835d-4218-bca6-b2be6a60044f)

final situation example
![最终](https://github.com/IndescribableMask/Danganronpa-V3-Dig-Game/assets/38174687/8a6b9512-e9ef-4785-a9e8-a02fa1c0a779)

### Tips

Different simulations may lead to different final results. If you want the results to be reproducible, please set a random seed.

During visualization, the already eliminated areas are represented by 'X', the areas yet to be eliminated are represented by '-', and the areas that need to be eliminated in the next step are represented by Chinese characters "白 粉 黄 蓝" correspond to 'white', 'pink', 'yellow', 'blue' respectively.

The simulation process cannot change with the appearance of bears or fish. 
If you have bad luck for rank S, please try again multiple times. 

Most simulation processes start from the top left corner, with a few cases starting from the bottom right corner.
There is a very small probability of simulation failure, in which case please start a new game.

Any questions, please leave Issues.



