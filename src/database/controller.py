from sqlmodel import Session, select
from typing import List, Optional
from src.database.models import Relatorios2024, engine

class RelatorioController:

    @staticmethod
    def create_relatorio(relatorio_data: Relatorios2024) -> Relatorios2024:
        with Session(engine) as session:
            session.add(relatorio_data)
            session.commit()
            session.refresh(relatorio_data)  # Refresh to get the generated ID
            return relatorio_data
    
    @staticmethod
    def create_relatories(relatories: List[Relatorios2024]):
        with Session(engine) as session:
            for relatorie in relatories:
                session.add(relatorie)
            session.commit()
            return True
    
    @staticmethod
    def get_relatorio_by_id(relatorio_id: int) -> Optional[Relatorios2024]:
        with Session(engine) as session:
            relatorio = session.get(Relatorios2024, relatorio_id)
            return relatorio

    @staticmethod
    def get_all_relatorios() -> List[Relatorios2024]:
        with Session(engine) as session:
            statement = select(Relatorios2024)
            results = session.exec(statement)
            return results.all()

    @staticmethod
    def update_relatorio(relatorio_id: int, new_data: Relatorios2024) -> Optional[Relatorios2024]:
        with Session(engine) as session:
            relatorio = session.get(Relatorios2024, relatorio_id)
            if relatorio:
                for key, value in new_data.dict(exclude_unset=True).items():
                    setattr(relatorio, key, value)
                session.add(relatorio)
                session.commit()
                session.refresh(relatorio)
            return relatorio

    @staticmethod
    def delete_relatorio(relatorio_id: int) -> bool:
        with Session(engine) as session:
            relatorio = session.get(Relatorios2024, relatorio_id)
            if relatorio:
                session.delete(relatorio)
                session.commit()
                return True
            return False
