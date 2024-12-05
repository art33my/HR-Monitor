from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .users import User
from .vacancies import Vacancy
from .stages import Stage
from .resumes import Resume
from .resume_stages import ResumeStage
from .sla import SLA
