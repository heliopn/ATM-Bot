from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class CrawlerDatabase:
    def __init__(self, db_name):
        self.engine = create_engine(f'sqlite:///{db_name}')
        self.Session = sessionmaker(bind=self.engine)
        self.Base = declarative_base()

        class Page(self.Base):
            __tablename__ = 'pages'

            id = Column(Integer, primary_key=True)
            url = Column(String)
            content = Column(String)

        self.Base.metadata.create_all(self.engine)

    def add_page(self, url, content):
        session = self.Session()
        page = Page(url=url, content=content)
        session.add(page)
        session.commit()
        session.close()

    def get_all_pages(self):
        session = self.Session()
        pages = session.query(Page).all()
        session.close()
        return pages

    def get_page_by_url(self, url):
        session = self.Session()
        page = session.query(Page).filter_by(url=url).first()
        session.close()
        return page