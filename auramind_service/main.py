"""
AuraMind LLM Agent - Micro-serviço FastAPI
Agente de IA para análise e sugestão de planejamentos pedagógicos.
Roda na porta 8001 e é chamado pelo sistema AuraClass.
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar aplicação FastAPI
app = FastAPI(
    title="AuraMind LLM Agent",
    description="Agente de IA para análise e sugestão de planejamentos pedagógicos",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# MODELOS PYDANTIC
# ============================================================================

class HabilidadeBNCC(BaseModel):
    """Modelo para habilidade BNCC"""
    codigo: str = Field(..., description="Código BNCC (ex: EF05LP01)")
    descricao: str = Field(..., description="Descrição da habilidade")


class SolicitacaoSugestao(BaseModel):
    """Modelo para requisição de sugestão de planejamento"""
    nivel_ensino: str = Field(..., description="Nível de ensino (1ef, 2ef, etc)")
    tema: str = Field(..., description="Tema do planejamento")
    habilidades_bncc: List[str] = Field(default=[], description="Códigos BNCC a trabalhar")
    duracao_semanas: int = Field(default=4, description="Duração em semanas")
    contexto_turma: Optional[str] = Field(None, description="Contexto específico da turma")


class SugestaoResposta(BaseModel):
    """Modelo para resposta de sugestão"""
    titulo: str
    introducao: str
    unidades_tematicas: List[Dict[str, Any]]
    atividades_sugeridas: List[Dict[str, Any]]
    recursos_necessarios: List[str]
    avaliacoes_propostas: List[str]
    score_aderencia_bncc: float
    observacoes: str


class RequisicaoAnalise(BaseModel):
    """Modelo para requisição de análise de plano"""
    plano_id: int = Field(..., description="ID do planejamento")
    titulo: str = Field(..., description="Título do plano")
    nivel_ensino: str = Field(..., description="Nível de ensino")
    habilidades_bncc: List[str] = Field(..., description="Habilidades BNCC")
    objetivos_aprendizagem: str = Field(..., description="Objetivos de aprendizagem")
    atividade_dirigida: str = Field(..., description="Atividade dirigida")
    desenvolvimento: str = Field(..., description="Desenvolvimento da aula")
    avaliacao: str = Field(..., description="Metodologia de avaliação")


class PontoAnalise(BaseModel):
    """Modelo para ponto de análise"""
    aspecto: str
    descricao: str
    impacto: str  # "alto", "médio", "baixo"


class AnaliseResposta(BaseModel):
    """Modelo para resposta de análise"""
    plano_id: int
    score_geral: float
    aderencia_bncc: float
    qualidade_pedagogica: float
    pontos_fortes: List[PontoAnalise]
    pontos_revisar: List[PontoAnalise]
    sugestoes_melhoria: List[str]
    recomendacao_final: str
    timestamp: str


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/health", tags=["Health"])
async def health_check():
    """Verificar saúde do serviço"""
    return {
        "status": "healthy",
        "service": "AuraMind LLM Agent",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.post(
    "/api/v1/auramind/sugestoes_planejamento/",
    response_model=SugestaoResposta,
    tags=["Planejamentos"],
    summary="Gerar sugestão de planejamento com IA"
)
async def sugerir_planejamento(requisicao: SolicitacaoSugestao):
    """
    Endpoint para gerar sugestões de planejamento pedagógico baseado em IA.
    
    Recebe:
    - Nível de ensino
    - Tema do planejamento
    - Habilidades BNCC desejadas
    - Duração em semanas
    - Contexto da turma
    
    Retorna:
    - Planejamento completo com unidades temáticas
    - Atividades sugeridas
    - Recursos necessários
    - Propostas de avaliação
    - Score de aderência à BNCC
    """
    try:
        logger.info(f"Gerando sugestão para tema: {requisicao.tema}")
        
        # Simular processamento de IA
        # Em produção, isso chamaria um modelo LLM real (GPT, Claude, etc)
        
        unidades_tematicas = [
            {
                "titulo": f"Unidade 1: Introdução ao {requisicao.tema}",
                "semanas": 1,
                "habilidades": requisicao.habilidades_bncc[:2] if requisicao.habilidades_bncc else ["EF05LP01"],
                "descricao": f"Apresentação e contextualização do tema {requisicao.tema}"
            },
            {
                "titulo": f"Unidade 2: Desenvolvimento de {requisicao.tema}",
                "semanas": 2,
                "habilidades": requisicao.habilidades_bncc[2:4] if len(requisicao.habilidades_bncc) > 2 else ["EF05LP02"],
                "descricao": f"Aprofundamento dos conceitos de {requisicao.tema}"
            },
            {
                "titulo": f"Unidade 3: Aplicação prática de {requisicao.tema}",
                "semanas": 1,
                "habilidades": requisicao.habilidades_bncc[4:] if len(requisicao.habilidades_bncc) > 4 else ["EF05LP03"],
                "descricao": f"Projetos e atividades práticas com {requisicao.tema}"
            }
        ]
        
        atividades_sugeridas = [
            {
                "titulo": "Atividade Dirigida: Exploração Inicial",
                "tipo": "exercicio",
                "duracao_min": 30,
                "habilidades": requisicao.habilidades_bncc[:1] if requisicao.habilidades_bncc else ["EF05LP01"]
            },
            {
                "titulo": "Projeto Colaborativo",
                "tipo": "projeto",
                "duracao_min": 120,
                "habilidades": requisicao.habilidades_bncc[1:3] if len(requisicao.habilidades_bncc) > 1 else ["EF05LP02"]
            },
            {
                "titulo": "Avaliação Formativa",
                "tipo": "quiz",
                "duracao_min": 45,
                "habilidades": requisicao.habilidades_bncc
            }
        ]
        
        recursos = [
            "Quadro branco e marcadores",
            "Computadores/tablets para pesquisa",
            "Materiais de arte e criatividade",
            "Livros e referências sobre o tema",
            "Acesso à internet"
        ]
        
        avaliacoes = [
            "Observação contínua das atividades",
            "Análise de participação em discussões",
            "Avaliação do projeto colaborativo",
            "Quiz de verificação de aprendizagem",
            "Autoavaliação do aluno"
        ]
        
        resposta = SugestaoResposta(
            titulo=f"Planejamento: {requisicao.tema} ({requisicao.nivel_ensino})",
            introducao=f"Este planejamento foi gerado pela IA AuraMind para o tema '{requisicao.tema}' no nível '{requisicao.nivel_ensino}'. "
                      f"Ele integra {len(requisicao.habilidades_bncc)} habilidades BNCC e está estruturado em {requisicao.duracao_semanas} semanas.",
            unidades_tematicas=unidades_tematicas,
            atividades_sugeridas=atividades_sugeridas,
            recursos_necessarios=recursos,
            avaliacoes_propostas=avaliacoes,
            score_aderencia_bncc=0.92,
            observacoes="Planejamento gerado automaticamente. Recomenda-se revisão e personalização conforme contexto da turma."
        )
        
        logger.info(f"Sugestão gerada com sucesso para tema: {requisicao.tema}")
        return resposta
        
    except Exception as e:
        logger.error(f"Erro ao gerar sugestão: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar sugestão: {str(e)}"
        )


@app.post(
    "/api/v1/auramind/analise_plano/",
    response_model=AnaliseResposta,
    tags=["Análises"],
    summary="Analisar plano pedagógico com IA"
)
async def analisar_plano(requisicao: RequisicaoAnalise):
    """
    Endpoint para análise de plano pedagógico usando IA.
    
    Recebe:
    - Dados completos do planejamento
    - Habilidades BNCC
    - Atividades e avaliações
    
    Retorna:
    - Score geral de qualidade
    - Aderência à BNCC
    - Qualidade pedagógica
    - Pontos fortes e fracos
    - Sugestões de melhoria
    - Recomendação final
    """
    try:
        logger.info(f"Analisando plano ID: {requisicao.plano_id}")
        
        # Simular análise de IA
        # Em produção, isso usaria um modelo LLM para análise real
        
        pontos_fortes = [
            PontoAnalise(
                aspecto="Alinhamento BNCC",
                descricao="O plano está bem alinhado com as habilidades BNCC especificadas",
                impacto="alto"
            ),
            PontoAnalise(
                aspecto="Estrutura Pedagógica",
                descricao="As atividades estão bem sequenciadas e progressivas",
                impacto="alto"
            ),
            PontoAnalise(
                aspecto="Diversidade de Metodologias",
                descricao="Uso de diferentes tipos de atividades (dirigidas, projetos, avaliações)",
                impacto="médio"
            )
        ]
        
        pontos_revisar = [
            PontoAnalise(
                aspecto="Tempo de Aula",
                descricao="Considere ajustar o tempo estimado para algumas atividades",
                impacto="médio"
            ),
            PontoAnalise(
                aspecto="Recursos Específicos",
                descricao="Detalhe melhor quais recursos serão necessários",
                impacto="baixo"
            )
        ]
        
        sugestoes = [
            "Adicione mais atividades de diferenciação para alunos com dificuldades",
            "Inclua estratégias de engajamento para manter a motivação",
            "Considere integrar tecnologia de forma mais significativa",
            "Aumente as oportunidades de feedback formativo"
        ]
        
        resposta = AnaliseResposta(
            plano_id=requisicao.plano_id,
            score_geral=0.88,
            aderencia_bncc=0.95,
            qualidade_pedagogica=0.85,
            pontos_fortes=pontos_fortes,
            pontos_revisar=pontos_revisar,
            sugestoes_melhoria=sugestoes,
            recomendacao_final="APROVADO COM OBSERVAÇÕES - Plano de boa qualidade. Recomenda-se implementar as sugestões de melhoria para otimizar a experiência de aprendizagem.",
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"Análise concluída para plano ID: {requisicao.plano_id}")
        return resposta
        
    except Exception as e:
        logger.error(f"Erro ao analisar plano: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar análise: {str(e)}"
        )


@app.get("/api/v1/auramind/status/", tags=["Status"])
async def status_auramind():
    """Retornar status do agente AuraMind"""
    return {
        "status": "online",
        "service": "AuraMind LLM Agent",
        "endpoints": {
            "sugestoes_planejamento": "/api/v1/auramind/sugestoes_planejamento/",
            "analise_plano": "/api/v1/auramind/analise_plano/",
            "health": "/health"
        },
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# ROOT
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Endpoint raiz com informações do serviço"""
    return {
        "message": "AuraMind LLM Agent - Bem-vindo!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
