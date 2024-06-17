from __future__ import annotations
from typing import Generic,TypeVar
from typing import Dict,Iterator,Dict,Tuple

class ClassNotFoundException(Exception):pass
class PackageNotFoundException(Exception):pass

package=TypeVar("package")
Class = TypeVar('Class')

class APIManager(Generic[Class]):
    
    Globals:Dict[str,type]={}
    
    def __init__(self,Type:Class) -> None:
        self.__type:type=Type
        self.__classes:Dict[str,type]={}
    
    def register(self,Target:Class):
        assert issubclass(Target,self.__type) and isinstance(Target,type)
        self.__classes[Target.__name__]=Target
        return Target
    
    def getClass(self,ClassName:str) -> Class:
        if ClassName in self.__classes:
            return self.__classes[ClassName]
        raise ClassNotFoundException(f"Class {ClassName} Not Found")
    
    @property
    def Type(self)->Class:
        return self.__type
    
    def iter(self) -> Iterator[Tuple[str,type]]:
        yield from self.__classes.items()

class Package(Generic[package]):
    def __init__(self,name:package,parent:Package=None) -> None:
        self.__name=name
        self.__parent=parent
        self.__sub_package:Dict[package,Package]={}
        self.__class_manager:Dict[Class,APIManager]={}
        print(repr(self))
    @property
    def Name(self):
        return self.__name
    
    @property
    def Parent(self):
        return self.__parent
    
    @property
    def Path(self):
        if not self.Parent:
            return self.Name
        return f"{self.Parent.Path}::{self.Name}"
    
    def __repr__(self) -> str:
        return f"package {self.Path}"
    
    def getAPIManager(self,Type:Class) -> APIManager[Class]:
        if not Type in self.__class_manager.keys():
            self.__class_manager[Type]=APIManager(Type)
        return self.__class_manager[Type]
    
    def getSubPackage(self,name:package) -> Package[package]:
        assert name
        if name in self.__sub_package.keys():
            return self.__sub_package[name]
        raise PackageNotFoundException(self.Name,name)
    
    def createSubPackage(self,name:package):
        if not name in self.__sub_package.keys():
            self.__sub_package[name]=Package(name,self)
        return self.__sub_package[name]
    
    def iterAPI(self) -> Iterator[Tuple[Class,APIManager]]:
        yield from self.__class_manager.items()
    
    def iterSubPackage(self) -> Iterator[Tuple[Class,APIManager]]:
        yield from self.__sub_package.items()

class PackageManager:
    
    root=Package("root")
    
    @classmethod
    def get(cls,path:str) -> Package:
        curr:Package=cls.root
        for name in path.split("::"):
            curr=curr.getSubPackage(name)
        return curr
    
    @classmethod
    def create(cls,path:str) -> Package:
        curr:Package=cls.root
        for name in path.split("::"):
            curr=curr.createSubPackage(name)
        return curr