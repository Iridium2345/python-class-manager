from __future__ import annotations
from typing import Any, Generic,TypeVar
from typing import Dict,Iterator,Dict,Tuple

class ClassNotFoundException(Exception):pass
class PackageNotFoundException(Exception):pass

package=TypeVar("package")
path=str
name=str
Class=TypeVar('Class')
Type=TypeVar('Type')

class APIManager(Generic[Class]):
    
    def __init__(self,Type:Class,package:Package) -> None:
        self.__type:type=Type
        self.__classes:Dict[str,type]={}
        self.__package=package
        
    def register(self,Target:Generic[Type]) -> Type:
        assert issubclass(Target,self.__type) and isinstance(Target,type)
        self.__classes[Target.__name__]=Target
        if hasattr(Target,"Aliases"):
            self.__classes[Target.Aliases]=Target
        Target.package=self.__package
        return Target
    
    def getClass(self,ClassName:str) -> Class:
        if ClassName in self.__classes.keys():
            return self.__classes[ClassName]
        raise ClassNotFoundException(f"Class {ClassName} Not Found")
    
    def exist(self,ClassName:str) -> bool:
        return ClassName in self.__classes.keys()
    
    @property
    def Type(self)->Class:
        return self.__type
    
    def iter(self) -> Iterator[Tuple[str,Class]]:
        yield from self.__classes.items()

class Package(Generic[package]):
    def __init__(self,name:package,parent:Package=None) -> None:
        self.__name=name
        self.__parent=parent
        self.__sub_package:Dict[package,Package]={}
        self.__class_manager:Dict[Class,APIManager]={}

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
    
    def __str__(self) -> str:
        return f"<package {self.Path}>"
    
    def show(self,level:int=0) -> str:
        tmp=[f"{' '*level}> {self}"]
        for api,Manager in self.iterAPI():
            tmp.append(f"{' '*(level+1)}> {api.__name__}")
            for name,clazz in Manager.iter():
                tmp.append(f"{' '*(level+2)}- {self.Path}::{name}")
        for name,sub in self.iterSubPackage():
            tmp.append(sub.show(level+1))
        return "\n".join(tmp)                
                
    def getAPIManager(self,Type:Class) -> APIManager[Class]:
        if not Type in self.__class_manager.keys():
            self.__class_manager[Type]=APIManager(Type,self)
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
    
    def iterAPI(self) -> Iterator[Tuple[Class,APIManager[Class]]]:
        yield from self.__class_manager.items()
    
    def iterSubPackage(self) -> Iterator[Tuple[str,Package]]:
        yield from self.__sub_package.items()

class PackageManager:
    
    root=Package("root")
    
    @classmethod
    def get(cls,path:str) -> Package:
        if not path:return cls.root
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
    
    @classmethod
    def __search(cls,package:Package,api:Class,name:str)->Class:
        if (manager:=package.getAPIManager(api)).exist(name):
            return manager.getClass(name)
        for _,sub in package.iterSubPackage():
            if tmp:=cls.__search(sub,api,name):
                return tmp
        return None
    
    @classmethod
    def search(cls,package:Package,api:Class,name:str) -> Class:
        if tmp:=cls.__search(package,api,name):
            return tmp
        raise ClassNotFoundException(f"Class {name} Not Found")
    
    @staticmethod
    def splitPath(path:str) -> Tuple[name,path]:
        if len(tmp:=path.split("::"))==1:
            return tmp[0],None
        return tmp[-1],"::".join(tmp[:-1]) 
    
    @classmethod
    def fromPath(cls,path:str,api:Class) -> Class:
        name,path=cls.splitPath(path)
        return cls.get(path).getAPIManager(api).getClass(name)
        
    @classmethod
    def iterAPI(cls,api:Class,package:Package=None) -> Iterator[Tuple[str,Class]]:
        if not package:package=cls.root
        for _,sub in package.iterSubPackage():
            yield from cls.iterAPI(api,sub)
        for name,clazz in package.getAPIManager(api).iter():
            yield f"{package.Path}::{name}",clazz
        return
        
        