from MiniGames.Pipeline.monobehaviour import MonoBehaviour
from MiniGames.Utils.color import Color
from MiniGames.Pipeline.gameobject import GameObject

class RendererBase(MonoBehaviour):
    def __init__(self, gameobject: GameObject):
        super(RendererBase, self).__init__(gameobject)
        self.__color = Color.White()

        self.transform.ADD_TO_ON_POS_CHANGE(self.RecalculatePos)
        self.transform.ADD_TO_ON_SCA_CHANGE(self.RecalculateScale)
        self.transform.ADD_TO_ON_ROT_CHANGE(self.RecalculateRot)

    @property
    def color(self) -> Color:
        return self.__color

    @color.setter
    def color(self, value: Color):
        if type(value) is not Color:
            raise TypeError()
        self.__color = value

    def RecalculateRot(self): raise NotImplementedError()
    def RecalculateScale(self): raise NotImplementedError()
    def RecalculatePos(self): raise NotImplementedError()
    def Render(self): raise NotImplementedError()

    def Enable(self):
        super(RendererBase, self).Enable()
        self.gameobject.AddTo("r", self)

    def Disable(self):
        super(RendererBase, self).Disable()
        self.gameobject.RemoveFrom("r", self)


