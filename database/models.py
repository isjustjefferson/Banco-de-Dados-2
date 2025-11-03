# database/models.py

import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from .connection import Base  # Importa a Base que criamos em connection.py

# --- Tabela de Associação (N:N) ---
# Esta é a nossa tabela de relacionamento Muitos-para-Muitos.
# Ela liga a tabela 'transacoes' com a tabela 'tags'.
# Não é uma classe, pois o SQLAlchemy vai gerenciá-la.
transacao_tag_association = Table(
    'transacao_tag', Base.metadata,
    Column('transacao_id', Integer, ForeignKey('transacoes.id_transacao'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id_tag'), primary_key=True)
)

# --- Nossas 10 Tabelas ---

# 1. Tabela: Usuario
class Usuario(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False) # Armazenará o hash (ex: bcrypt)
    data_criacao = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    # Relacionamentos (O que este usuário "possui")
    contas = relationship('Conta', back_populates='usuario')
    orcamentos = relationship('Orcamento', back_populates='usuario')
    metas = relationship('Meta', back_populates='usuario')

    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, nome='{self.nome}')>"

# 2. Tabela: Conta
class Conta(Base):
    __tablename__ = 'contas'
    id_conta = Column(Integer, primary_key=True, autoincrement=True)
    nome_conta = Column(String(100), nullable=False) # Ex: "Carteira", "Banco Nu", "Cartão Visa"
    tipo_conta = Column(String(50)) # Ex: "Corrente", "Poupança", "Crédito"
    saldo_inicial = Column(Float, default=0.0)
    
    # Chave Estrangeira (A quem esta conta "pertence")
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    
    # Relacionamentos
    usuario = relationship('Usuario', back_populates='contas')
    transacoes = relationship('Transacao', back_populates='conta')
    investimentos = relationship('Investimento', back_populates='conta')

    def __repr__(self):
        return f"<Conta(id={self.id_conta}, nome='{self.nome_conta}')>"

# 3. Tabela: Categoria
class Categoria(Base):
    __tablename__ = 'categorias'
    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), unique=True, nullable=False) # Ex: "Alimentação", "Transporte", "Salário"
    tipo = Column(String(20), nullable=False) # "Receita" ou "Despesa"

    # Relacionamentos
    transacoes = relationship('Transacao', back_populates='categoria')
    orcamentos = relationship('Orcamento', back_populates='categoria')
    
    def __repr__(self):
        return f"<Categoria(id={self.id_categoria}, nome='{self.nome}')>"

# 4. Tabela: Transacao
class Transacao(Base):
    __tablename__ = 'transacoes'
    id_transacao = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255))
    valor = Column(Float, nullable=False)
    data = Column(Date, nullable=False, default=datetime.date.today)
    
    # Chaves Estrangeiras
    id_conta = Column(Integer, ForeignKey('contas.id_conta'), nullable=False)
    id_categoria = Column(Integer, ForeignKey('categorias.id_categoria'), nullable=False)
    
    # Relacionamentos
    conta = relationship('Conta', back_populates='transacoes')
    categoria = relationship('Categoria', back_populates='transacoes')
    
    # Relacionamento N:N com Tag
    tags = relationship('Tag', secondary=transacao_tag_association, back_populates='transacoes')

    def __repr__(self):
        return f"<Transacao(id={self.id_transacao}, valor={self.valor})>"

# 5. Tabela: Tag
class Tag(Base):
    __tablename__ = 'tags'
    id_tag = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), unique=True, nullable=False) # Ex: "Férias", "Imposto"

    # Relacionamento N:N com Transacao
    transacoes = relationship('Transacao', secondary=transacao_tag_association, back_populates='tags')

    def __repr__(self):
        return f"<Tag(id={self.id_tag}, nome='{self.nome}')>"

# (A 6ª tabela é a 'transacao_tag_association', que já definimos no topo)

# 7. Tabela: Orcamento
class Orcamento(Base):
    __tablename__ = 'orcamentos'
    id_orcamento = Column(Integer, primary_key=True, autoincrement=True)
    valor_planejado = Column(Float, nullable=False)
    mes = Column(Integer, nullable=False) # 1 = Jan, 12 = Dez
    ano = Column(Integer, nullable=False)
    
    # Chaves Estrangeiras
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    id_categoria = Column(Integer, ForeignKey('categorias.id_categoria'), nullable=False)
    
    # Relacionamentos
    usuario = relationship('Usuario', back_populates='orcamentos')
    categoria = relationship('Categoria', back_populates='orcamentos')

    def __repr__(self):
        return f"<Orcamento(cat_id={self.id_categoria}, valor={self.valor_planejado})>"

# 8. Tabela: Meta
class Meta(Base):
    __tablename__ = 'metas'
    id_meta = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False) # Ex: "Viagem Japão"
    valor_objetivo = Column(Float, nullable=False)
    valor_atual = Column(Float, default=0.0)
    data_limite = Column(Date)
    
    # Chave Estrangeira
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    
    # Relacionamento
    usuario = relationship('Usuario', back_populates='metas')

    def __repr__(self):
        return f"<Meta(id={self.id_meta}, nome='{self.nome}')>"

# 9. Tabela: TipoInvestimento
class TipoInvestimento(Base):
    __tablename__ = 'tipos_investimento'
    id_tipo_investimento = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), unique=True, nullable=False) # Ex: "Ação", "Fundo Imobiliário", "CDB"
    
    # Relacionamento
    investimentos = relationship('Investimento', back_populates='tipo_investimento')

    def __repr__(self):
        return f"<TipoInvestimento(nome='{self.nome}')>"

# 10. Tabela: Investimento
class Investimento(Base):
    __tablename__ = 'investimentos'
    id_investimento = Column(Integer, primary_key=True, autoincrement=True)
    simbolo = Column(String(20)) # Ex: "PETR4", "MXRF11"
    quantidade = Column(Float)
    preco_medio = Column(Float)
    
    # Chaves Estrangeiras
    id_conta = Column(Integer, ForeignKey('contas.id_conta'), nullable=False)
    id_tipo_investimento = Column(Integer, ForeignKey('tipos_investimento.id_tipo_investimento'), nullable=False)
    
    # Relacionamentos
    conta = relationship('Conta', back_populates='investimentos')
    tipo_investimento = relationship('TipoInvestimento', back_populates='investimentos')

    def __repr__(self):
        return f"<Investimento(simbolo='{self.simbolo}', qtd={self.quantidade})>"