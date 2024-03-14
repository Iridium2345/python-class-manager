from typing import Generic,TypeVar,Generator,Any

Class = TypeVar('Class')

class ClassNotFoundException(Exception):pass

class _ClassManager(Generic[Class]):
    def __init__(self,TargetType:Class) -> None:
        self.__TargetType=TargetType
        self.__Commands={}
    
    def register(self,Target:Class):
        assert issubclass(Target,self.__TargetType)
        self.__Commands[Target.__name__]=Target
        return Target
    
    def getClass(self,ClassName:str) -> Class:
        if(ClassName in self.__Commands.keys()):
            return self.__Commands[ClassName]
        raise ClassNotFoundException(f"Class {ClassName} Not Found")
    
    def getType(self)->Class:
        return self.__TargetType
    
    def getAllClass(self)->Generator[Any,Any,Class]:
        yield from self.__Commands.values()
    
    def getAllName(self)->Generator[Any,Any,str]:
        yield from self.__Commands.keys()

class ClassManager:
    __instance={}
    
    @classmethod
    def getManager(cls,TargetType:Class)-> _ClassManager[Class]:
        if not TargetType in cls.__instance.keys():
            cls.__instance[TargetType]=_ClassManager(TargetType)
        return cls.__instance[TargetType]
    
    @classmethod
    def getAll(cls)->Generator[Any,Any,_ClassManager[Class]]:
        yield from cls.__instance.values()