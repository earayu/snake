# snake

好气啊,这个贪吃蛇算法是自己构思和实现的：
一条蛇由N个节点构成，每个节点有2个属性，“当前方向”和“上一个方向”。后一个节点的方向为上一个节点的上一个方向，由此实现蛇的移动。
吃到苹果的话在结尾增加一个节点


然后看了一下别人的贪吃蛇算法：
每次移动都在蛇的最前面加上一个节点，然后删除最后一个节点，吃到苹果则不删除。这样就根本不用考虑蛇（除了蛇头）的方向。厉害了