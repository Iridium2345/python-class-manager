from typing import Generic,TypeVar,Generator,Any,Dict,Tuple

Class = TypeVar('Class')

class ClassNotFoundException(Exception):pass

class _ClassManager(Generic[Class]):
    def __init__(self,TargetType:Class) -> None:
        self.__TargetType=TargetType
        self.__Commands:Dict[Tuple[str,str]]={}
    
    def register(self,package:str):
        def register(Target:Class):
            assert issubclass(Target,self.__TargetType)
            self.__Commands[(f"{package}.{Target.__name__}",Target.__name__)]=Target
            return Target
        return register
    
    def getClass(self,ClassName:str) -> Class:
        for key in self.__Commands.keys():
            if(ClassName in key):
                return self.__Commands[key]
        raise ClassNotFoundException(f"Class {ClassName} Not Found")
    
    def getType(self)->Class:
        return self.__TargetType
    
    def getAllClass(self)->Generator[Any,Any,Class]:
        yield from self.__Commands.values()
    
    def getAllName(self)->Generator[Any,Any,Tuple[str,str]]:
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