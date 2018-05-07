# -*- coding: utf-8 -*-
#!/usr/bin/python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class JobData(DeclarativeBase):
    __tablename__ = "JobData"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    RecordTime = Column(String(255), index=True)
    JobUUID = Column(String(255), index=True)
    CityName = Column(String(255), index=True)
    CityCode = Column(String(255))
    JobTitle = Column(String(255), index=True)
    Pay = Column(String(255))
    Region = Column(String(255))
    WorkYears = Column(String(255))
    Education = Column(String(255))
    Industry = Column(String(255))
    Financing = Column(String(255))
    People = Column(String(255))
    Company = Column(String(255))
    CompanyUrl = Column(String(255))
    Publisher = Column(String(255))
    PublisherPosition = Column(String(255))
    ReleaseTime = Column(String(255))
    Ka = Column(String(255))
    DataJid = Column(String(255))
    DataLid = Column(String(255))
    JobDetail = Column(String(4096))
    CompanyDetail = Column(String(4096))
    CompanyName = Column(String(255))
    LegalRepresentative = Column(String(255))
    RegisteredCapital = Column(String(255))
    ResTime = Column(String(255))
    CompanyType = Column(String(255))
    ManageState = Column(String(255))
    LoactionAddress = Column(String(255))
