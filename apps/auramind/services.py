"""
Services for AuraMind app - IA Integration.
"""
import requests
import time
import logging
from django.conf import settings
from .models import SugestaoIa, AnaliseIa, LogIa

logger = logging.getLogger(__name__)


class AuraMindService:
    """
    Service to interact with AuraMind IA Agent.
    """
    
    def __init__(self):
        self.base_url = settings.AURAMIND_API_URL
        self.api_key = settings.AURAMIND_API_KEY
        self.timeout = 60
    
    def _get_headers(self):
        """Get request headers with authentication."""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def _log_interaction(self, usuario, tipo, entrada, saida, sucesso, tempo_ms, custo_token=0, erro=None):
        """Log IA interaction."""
        LogIa.objects.create(
            usuario=usuario,
            tipo=tipo,
            entrada=entrada,
            saida=saida,
            sucesso=sucesso,
            tempo_resposta_ms=tempo_ms,
            custo_token=custo_token,
            mensagem_erro=erro or ''
        )
    
    def gerar_sugestao_planejamento(self, professor, plano_data):
        """
        Generate pedagogical suggestion using AuraMind.
        """
        inicio = time.time()
        
        try:
            headers = self._get_headers()
            
            payload = {
                'plano_id': plano_data.get('plano_id'),
                'professor_id': professor.id,
                'nivel_ensino': plano_data.get('nivel_ensino'),
                'habilidade_foco': plano_data.get('habilidade_foco'),
                'contexto_previo': plano_data.get('contexto_previo'),
                'formato_desejado': plano_data.get('formato_desejado', 'atividade'),
                'parametros_adicionais': plano_data.get('parametros_adicionais', {})
            }
            
            response = requests.post(
                f'{self.base_url}sugestoes_planejamento/',
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            tempo_ms = int((time.time() - inicio) * 1000)
            
            if response.status_code == 200:
                resultado = response.json()
                
                # Save suggestion to database
                sugestao = SugestaoIa.objects.create(
                    professor=professor,
                    plano_id=plano_data.get('plano_id'),
                    habilidade_foco=plano_data.get('habilidade_foco'),
                    nivel_ensino=plano_data.get('nivel_ensino'),
                    tipo=plano_data.get('formato_desejado', 'atividade'),
                    contexto_previo=plano_data.get('contexto_previo'),
                    status='concluida',
                    titulo_sugestao=resultado.get('dados_sugeridos', {}).get('titulo'),
                    conteudo_sugestao=resultado.get('dados_sugeridos', {}).get('sugestao_texto'),
                    habilidades_sugeridas=resultado.get('dados_sugeridos', {}).get('habilidades_sugeridas', []),
                    custo_token=resultado.get('metadata', {}).get('custo_token', 0),
                    tempo_processamento_ms=resultado.get('metadata', {}).get('tempo_processamento_ms', tempo_ms),
                    modelo_ia=resultado.get('metadata', {}).get('modelo_ia', 'AuraMind-v3')
                )
                
                # Log interaction
                self._log_interaction(
                    usuario=professor,
                    tipo='sugestao',
                    entrada=payload,
                    saida=resultado,
                    sucesso=True,
                    tempo_ms=tempo_ms,
                    custo_token=resultado.get('metadata', {}).get('custo_token', 0)
                )
                
                logger.info(f"Sugestão gerada com sucesso para professor {professor.id}")
                return resultado
            else:
                erro_msg = f"Erro na API AuraMind: {response.status_code}"
                self._log_interaction(
                    usuario=professor,
                    tipo='sugestao',
                    entrada=payload,
                    saida={'error': response.text},
                    sucesso=False,
                    tempo_ms=tempo_ms,
                    erro=erro_msg
                )
                logger.error(erro_msg)
                raise Exception(erro_msg)
        
        except Exception as e:
            tempo_ms = int((time.time() - inicio) * 1000)
            self._log_interaction(
                usuario=professor,
                tipo='sugestao',
                entrada=plano_data,
                saida={},
                sucesso=False,
                tempo_ms=tempo_ms,
                erro=str(e)
            )
            logger.error(f"Erro ao gerar sugestão: {str(e)}")
            raise
    
    def analisar_plano(self, professor, plano_data):
        """
        Analyze planning using AuraMind.
        """
        inicio = time.time()
        
        try:
            headers = self._get_headers()
            
            payload = {
                'plano_id': plano_data.get('plano_id'),
                'nivel_ensino': plano_data.get('nivel_ensino'),
                'introducao_geral': plano_data.get('introducao_geral'),
                'unidades_tematicas': plano_data.get('unidades_tematicas', []),
                'instrucao_analise': 'Analise a aderência curricular (BNCC) e o nível de profundidade pedagógica. Gere um resumo com 3 pontos fortes e 3 pontos a revisar.'
            }
            
            response = requests.post(
                f'{self.base_url}analise_plano/',
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            tempo_ms = int((time.time() - inicio) * 1000)
            
            if response.status_code == 200:
                resultado = response.json()
                
                # Save analysis to database
                analise = AnaliseIa.objects.create(
                    professor=professor,
                    plano_id=plano_data.get('plano_id'),
                    tipo_analise='aderencia_curricular',
                    status='concluida',
                    pontos_fortes=resultado.get('analise', {}).get('pontos_fortes', []),
                    pontos_a_revisar=resultado.get('analise', {}).get('pontos_a_revisar', []),
                    recomendacoes=resultado.get('analise', {}).get('recomendacoes', ''),
                    score_aderencia=resultado.get('analise', {}).get('score_aderencia'),
                    custo_token=resultado.get('custo_token', 0)
                )
                
                # Log interaction
                self._log_interaction(
                    usuario=professor,
                    tipo='analise',
                    entrada=payload,
                    saida=resultado,
                    sucesso=True,
                    tempo_ms=tempo_ms,
                    custo_token=resultado.get('custo_token', 0)
                )
                
                logger.info(f"Análise realizada com sucesso para professor {professor.id}")
                return resultado
            else:
                erro_msg = f"Erro na API AuraMind: {response.status_code}"
                self._log_interaction(
                    usuario=professor,
                    tipo='analise',
                    entrada=payload,
                    saida={'error': response.text},
                    sucesso=False,
                    tempo_ms=tempo_ms,
                    erro=erro_msg
                )
                logger.error(erro_msg)
                raise Exception(erro_msg)
        
        except Exception as e:
            tempo_ms = int((time.time() - inicio) * 1000)
            self._log_interaction(
                usuario=professor,
                tipo='analise',
                entrada=plano_data,
                saida={},
                sucesso=False,
                tempo_ms=tempo_ms,
                erro=str(e)
            )
            logger.error(f"Erro ao analisar plano: {str(e)}")
            raise
