from datetime import datetime, date

from sqlalchemy import String, ForeignKey, Text, DateTime, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column


class Base(DeclarativeBase):
    ...


# ------------------------------------------------------------------------------------------------------
class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)

    employees: Mapped[list["Employee"]] = relationship(
        "Employee",
        secondary="participations",
        back_populates="projects"
    )


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    projects: Mapped[list["Project"]] = relationship(
        "Project",
        secondary="participations",
        back_populates="employees"
    )


class Participation(Base):
    __tablename__ = "participations"

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), primary_key=True)
    role: Mapped[str] = mapped_column(String(50), nullable="False")


# ------------------------------------------------------------------------------------------------------
class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="article_tags",
        back_populates="articles"
    )


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    articles: Mapped[list["Article"]] = relationship(
        "Article",
        secondary="article_tags",
        back_populates="tags"
    )


class ArticleTag(Base):
    __tablename__ = "article_tags"

    article_id: Mapped[str] = mapped_column(ForeignKey("articles.id"), primary_key=True)
    tag_id: Mapped[str] = mapped_column(ForeignKey("tags.id"), primary_key=True)


# ------------------------------------------------------------------------------------------------------
class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="comments")


# ------------------------------------------------------------------------------------------------------
class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    student_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="student")


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int] = mapped_column(nullable=False)
    subject: Mapped[str] = mapped_column(String(50), nullable=False)
    studetn_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)

    student: Mapped["Student"] = relationship("Student", back_populates="grades")
# ------------------------------------------------------------------------------------------------------

