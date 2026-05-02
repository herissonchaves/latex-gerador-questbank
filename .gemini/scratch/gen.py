import random

def get_id():
    return str(random.randint(100000, 999999))

questions = [
    {
        "id": get_id(),
        "tipo": "discursiva",
        "banca": "Desconhecida",
        "ano": "0",
        "disciplina": "Física",
        "topico": "Ondulatória",
        "conteudo": "Propriedades das Ondas",
        "assunto": "Comprimento de onda e período",
        "dificuldade": "medio",
        "enunciado": "Considere duas estações de rádio FM. A rádio Esperança opera com frequência de 90 MHz, enquanto a rádio Viva transmite em 100 MHz. Qual das estações emite ondas com maior comprimento de onda e qual emite ondas com menor período?\n\n\\textbf{Dado:} as ondas de rádio se propagam no ar com velocidade de aproximadamente $3{,}0 \\times 10^8\\,\\text{m/s}$.",
        "alternativas": [],
        "gabarito": "Esperança tem maior comprimento de onda. Viva tem menor período.",
        "enunciado_adaptado": "Temos duas estações de rádio: Esperança (90 MHz) e Viva (100 MHz). Ondas de rádio viajam pelo ar.\n\n\\textbf{Qual dessas estações tem o maior comprimento de onda e qual tem o menor período?}",
        "alternativas_adaptadas": [],
        "gabarito_adaptado": "Esperança e Viva, respectivamente.",
        "imagem_adaptada": ""
    },
    {
        "id": get_id(),
        "tipo": "discursiva",
        "banca": "Desconhecida",
        "ano": "0",
        "disciplina": "Física",
        "topico": "Ondulatória",
        "conteudo": "Propriedades das Ondas",
        "assunto": "Velocidade de propagação",
        "dificuldade": "medio",
        "enunciado": "Duas boias sinalizadoras emitem sinais captados por um sonar passivo posicionado sob o casco de um navio que realiza uma expedição marítima. A boia A transmite sinais a uma frequência de 2,0 MHz, e a boia B, a uma frequência de 5,0 MHz. Considerando que as ondas sonoras se propagam na água do mar com velocidade de $1{,}5 \\times 10^3\\,\\text{m/s}$, qual é a razão entre os comprimentos de onda das ondas emitidas pela boia A e pela boia B?",
        "alternativas": [],
        "gabarito": "2,5",
        "enunciado_adaptado": "Duas boias no mar emitem sinais para um navio. A boia A emite a 2,0 MHz e a boia B a 5,0 MHz. O som viaja na água com certa velocidade constante.\n\n\\textbf{Qual é a proporção (razão) entre o comprimento da onda da boia A e o da boia B?}",
        "alternativas_adaptadas": [],
        "gabarito_adaptado": "2,5",
        "imagem_adaptada": ""
    },
    {
        "id": get_id(),
        "tipo": "discursiva",
        "banca": "Desconhecida",
        "ano": "0",
        "disciplina": "Física",
        "topico": "Ondulatória",
        "conteudo": "Cordas Vibrantes",
        "assunto": "Equação de Taylor",
        "dificuldade": "dificil",
        "enunciado": "Ao tocar a corda de uma guitarra cujo braço tem comprimento L = 0,6 m, um músico produz uma onda representada pela figura a seguir.\n\n\\imagem{Imagem1.png}\n\nSe a corda tem densidade linear $\\mu = 5{,}0 \\times 10^{-3}\\,\\text{kg/m}$ e está submetida a uma tração de F = 100 N, qual é a frequência do som emitido?",
        "alternativas": [],
        "gabarito": "250 Hz",
        "enunciado_adaptado": "\\imagem{Imagem1.png}\n\nA figura mostra o desenho de uma onda formada na corda de uma guitarra ao ser tocada. Essa corda tem um comprimento e peso específicos.\n\n\\textbf{Qual é a frequência do som emitido pela corda, considerando a força aplicada nela?}",
        "alternativas_adaptadas": [],
        "gabarito_adaptado": "250 Hz",
        "imagem_adaptada": ""
    },
    {
        "id": get_id(),
        "tipo": "objetiva",
        "banca": "IFSUL",
        "ano": "0",
        "disciplina": "Física",
        "topico": "Ondulatória",
        "conteudo": "Características das Ondas",
        "assunto": "Meios de Propagação",
        "dificuldade": "medio",
        "enunciado": "De acordo com a teoria ondulatória, analise as afirmações abaixo.\n\nI. A velocidade de onda emitida por uma fonte depende do meio de propagação.\n\nII. Uma onda é uma perturbação que sempre necessita de um meio material para se propagar.\n\nIII. O som é uma onda de natureza eletromagnética.\n\nEstá(ão) correta(s) apenas a(s) afirmativa(s):",
        "alternativas": ["I.", "II.", "III.", "I e III."],
        "gabarito": "A",
        "enunciado_adaptado": "Ondas podem viajar por diferentes materiais. Algumas ondas, como a luz, podem viajar até no espaço vazio.\n\n\\textbf{Sobre as ondas e como elas viajam, o que é correto afirmar?}",
        "alternativas_adaptadas": ["A velocidade da onda depende do material (meio) por onde ela passa.", "Toda onda precisa de um material físico para conseguir viajar.", "O som é uma onda parecida com a luz (eletromagnética)."],
        "gabarito_adaptado": "A",
        "imagem_adaptada": ""
    },
    {
        "id": get_id(),
        "tipo": "objetiva",
        "banca": "PUCCAMP",
        "ano": "0",
        "disciplina": "Física",
        "topico": "Ondulatória",
        "conteudo": "Tipos de Ondas",
        "assunto": "Ondas Mecânicas e Eletromagnéticas",
        "dificuldade": "facil",
        "enunciado": "Os sistemas visual e auditivo humanos captam ondas que se propagam no ambiente, mas cada sistema é sensível a determinado tipo de onda, as quais possuem diferentes características. Enquanto as ondas sonoras são \\underline{\\quad\\quad I \\quad\\quad} e \\underline{\\quad\\quad II \\quad\\quad}, as ondas luminosas são \\underline{\\quad\\quad III \\quad\\quad} e \\underline{\\quad\\quad IV \\quad\\quad}.\n\nAs palavras que completam corretamente as lacunas I, II, III e IV são, respectivamente,",
        "alternativas": ["mecânicas --- transversais --- eletromagnéticas --- longitudinais.", "mecânicas --- longitudinais --- eletromagnéticas --- transversais.", "mecânicas --- transversais --- mecânicas --- longitudinais.", "eletromagnéticas --- transversais --- eletromagnéticas --- longitudinais.", "eletromagnéticas --- longitudinais --- mecânicas --- transversais."],
        "gabarito": "B",
        "enunciado_adaptado": "Nossos olhos captam a luz e nossos ouvidos captam o som. Cada um deles é um tipo diferente de onda.\n\n\\textbf{Como classificamos, respectivamente, a onda do som e a onda da luz?}",
        "alternativas_adaptadas": ["Som é mecânico e longitudinal; luz é eletromagnética e transversal.", "Som é mecânico e transversal; luz é mecânica e longitudinal.", "Som é eletromagnético; luz é mecânica."],
        "gabarito_adaptado": "A",
        "imagem_adaptada": ""
    },
    {
        "id": get_id(),
        "tipo": "objetiva",
        "banca": "UFRGS",
        "ano": "0",
        "disciplina": "Física",
        "topico": "Ondulatória",
        "conteudo": "Propagação de Ondas",
        "assunto": "Onda Longitudinal",
        "dificuldade": "medio",
        "enunciado": "Assinale a alternativa que preenche corretamente as lacunas do enunciado abaixo, na ordem em que aparecem.\n\nNa propagação de uma onda mecânica longitudinal, o meio é deslocado \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_ à direção de propagação, \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_ ao transporte de energia. Nessa propagação \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_ transporte de matéria.",
        "alternativas": ["paralelamente --- perpendicular --- ocorre", "paralelamente --- paralela --- ocorre", "paralelamente --- paralela --- não ocorre", "perpendicularmente --- paralela --- não ocorre", "perpendicularmente --- perpendicular --- não ocorre"],
        "gabarito": "C",
        "enunciado_adaptado": "Em uma onda do tipo longitudinal, a vibração do material acompanha o sentido em que a onda está indo.\n\n\\textbf{Nesse tipo de onda, como é o deslocamento e o que é transportado?}",
        "alternativas_adaptadas": ["Vibra paralelo à onda, e não transporta matéria.", "Vibra de forma cruzada, e transporta matéria.", "Vibra paralelo à onda, e transporta matéria."],
        "gabarito_adaptado": "A",
        "imagem_adaptada": ""
    },
    {
        "id": get_id(),
        "tipo": "objetiva",
        "banca": "FCMSCSP",
        "ano": "0",
        "disciplina": "Física",
        "topico": "Ondulatória",
        "conteudo": "Ondas Sonoras",
        "assunto": "Velocidade do Som",
        "dificuldade": "medio",
        "enunciado": "O gráfico mostra como a velocidade de propagação das ondas sonoras no ar varia com a temperatura desse meio.\n\n\\imagem{Imagem2.png}\n\nSe uma onda sonora de frequência 200 Hz se propaga no ar com comprimento de onda de 1,84 m, a temperatura do ar é, aproximadamente,",
        "alternativas": ["$40\\,^{\\circ}\\text{C}$.", "$0\\,^{\\circ}\\text{C}$.", "$60\\,^{\\circ}\\text{C}$.", "$20\\,^{\\circ}\\text{C}$.", "$-20\\,^{\\circ}\\text{C}$."],
        "gabarito": "D",
        "enunciado_adaptado": "\\imagem{Imagem2.png}\n\nO gráfico mostra que o som viaja mais rápido no ar quando a temperatura está mais alta. Uma onda sonora específica de 200 Hz possui um comprimento de 1,84 metros.\n\n\\textbf{Observando os dados e o gráfico, qual é a temperatura do ar nesse momento?}",
        "alternativas_adaptadas": ["$20\\,^{\\circ}\\text{C}$.", "$0\\,^{\\circ}\\text{C}$.", "$-20\\,^{\\circ}\\text{C}$."],
        "gabarito_adaptado": "A",
        "imagem_adaptada": ""
    },
    {
        "id": get_id(),
        "tipo": "objetiva",
        "banca": "FICSAE",
        "ano": "0",
        "disciplina": "Física",
        "topico": "Ondulatória",
        "conteudo": "Propriedades das Ondas",
        "assunto": "Onda Transversal",
        "dificuldade": "facil",
        "enunciado": "A figura mostra uma corda na qual se propaga uma onda transversal. As cristas e os vales dessa onda estão todos contidos no plano \\textbf{xy} e a velocidade de propagação da onda tem a mesma direção e o mesmo sentido do eixo \\textbf{x}.\n\n\\imagem{Imagem3.png}\n\nCom relação à direção de oscilação dos pontos dessa corda e à matéria transportada pela onda, tem-se que todos os pontos da corda, atingidos pela onda, oscilam",
        "alternativas": ["nas direções \\textbf{x} e \\textbf{y} e, enquanto se propaga, a onda não transporta matéria.", "apenas na direção \\textbf{y} e, enquanto se propaga, a onda transporta matéria.", "nas direções \\textbf{x} e \\textbf{y} e, enquanto se propaga, a onda transporta matéria.", "apenas na direção \\textbf{x} e, enquanto se propaga, a onda não transporta matéria.", "apenas na direção \\textbf{y} e, enquanto se propaga, a onda não transporta matéria."],
        "gabarito": "E",
        "enunciado_adaptado": "\\imagem{Imagem3.png}\n\nA figura ilustra uma onda transversal em uma corda, com o eixo vertical y marcando a altura da vibração e o horizontal x a direção da onda.\n\n\\textbf{Nesse caso, para qual lado a corda se mexe (oscila) e o que a onda carrega consigo?}",
        "alternativas_adaptadas": ["Mexem apenas para cima e para baixo (eixo y) e não carregam matéria.", "Mexem para os lados (eixo x) e carregam a corda junto.", "Mexem para todas as direções (x e y) e transportam a corda."],
        "gabarito_adaptado": "A",
        "imagem_adaptada": ""
    },
    {
        "id": get_id(),
        "tipo": "objetiva",
        "banca": "FUVEST",
        "ano": "2024",
        "disciplina": "Física",
        "topico": "Ondulatória",
        "conteudo": "Matemática das Ondas",
        "assunto": "Função de Onda",
        "dificuldade": "dificil",
        "enunciado": "As enchentes ocorridas no Rio Grande do Sul, em maio de 2024, prejudicaram a infraestrutura de comunicação. A população afetada era informada sobre as notícias relativas às enchentes ao sintonizar, por rádio de pilhas, frequências de onda AM, cujo alcance é maior. Uma onda AM é modelada matematicamente por equações que envolvem a função cosseno, cuja variável independente é o tempo \\textbf{t}, que aparece multiplicado pela frequência \\textbf{f} da onda. Como exemplo, pode-se considerar a equação referente ao processo de modulação de uma onda AM:\n\n$s(t) = A[1 + k\\cdot m(t)] \\cos(2\\pi f t)$\n\nEm que A é a amplitude, \\textbf{f} a frequência, \\textbf{k} a constante da sensibilidade à amplitude e $m(t)$ o sinal que contém a informação.\n\nQuando a frequência \\textbf{f} é multiplicada por 3, o comprimento da onda sofre alteração. Por causa dessa multiplicação, qual transformação ocorre no gráfico da função cosseno original?",
        "alternativas": ["Expansão vertical.", "Translação horizontal.", "Expansão horizontal.", "Contração horizontal.", "Contração vertical."],
        "gabarito": "D",
        "enunciado_adaptado": "Rádios de onda AM foram muito usados nas enchentes porque o sinal viaja mais longe. O desenho matemático (gráfico) dessas ondas depende da frequência (velocidade de vibração).\n\n\\textbf{Se a frequência da onda for triplicada (ficar 3 vezes maior), o que acontece com a aparência do seu gráfico de onda no papel?}",
        "alternativas_adaptadas": ["Ele sofre uma contração horizontal, ficando mais apertado.", "Ele sofre uma expansão horizontal, ficando mais esticado.", "Ele sofre uma expansão vertical, ficando mais alto."],
        "gabarito_adaptado": "A",
        "imagem_adaptada": ""
    },
    {
        "id": get_id(),
        "tipo": "objetiva",
        "banca": "UFRGS",
        "ano": "0",
        "disciplina": "Física",
        "topico": "Ondulatória",
        "conteudo": "Propriedades das Ondas",
        "assunto": "Comprimento de onda",
        "dificuldade": "medio",
        "enunciado": "Em uma corda esticada com certa tensão constante, três ondas são enviadas separadamente. A figura abaixo representa as ondas, identificadas por 1, 2 e 3.\n\n\\imagem{Imagem4.png}\n\nAs razões entre os comprimentos de onda $\\lambda_1/\\lambda_2$, $\\lambda_1/\\lambda_3$ e $\\lambda_2/\\lambda_3$ dessas ondas são, respectivamente,",
        "alternativas": ["4/3, 2/3, 1/2.", "4/3, 3/2, 1/2.", "3/4, 2/3, 2.", "3/4, 3/2, 2.", "3/4, 3/2, 1/2."],
        "gabarito": "D",
        "enunciado_adaptado": "\\imagem{Imagem4.png}\n\nO diagrama exibe três ondas desenhadas juntas, permitindo ver qual delas tem o ciclo mais comprido.\n\n\\textbf{Analisando a largura (comprimento) das ondas, qual é a proporção entre a largura da onda 1 comparada à da onda 2?}",
        "alternativas_adaptadas": ["3 para 4 (3/4).", "4 para 3 (4/3).", "Metade (1/2)."],
        "gabarito_adaptado": "A",
        "imagem_adaptada": ""
    },
    {
        "id": get_id(),
        "tipo": "objetiva",
        "banca": "UFMS",
        "ano": "0",
        "disciplina": "Física",
        "topico": "Ondulatória",
        "conteudo": "Propriedades das Ondas",
        "assunto": "Período e Comprimento",
        "dificuldade": "medio",
        "enunciado": "Uma boia em alto-mar fica flutuando estática em relação à vertical, enquanto as ondas passam por ela. No instante $T_0$ a boia se encontra em uma crista e no instante $T_1$, pela segunda vez, em um vale.\n\n\\imagem{Imagem5.png}\n\nSabendo que em alto-mar as ondas estão se deslocando com velocidade de $15\\,\\text{m/s}$, o comprimento da onda é:",
        "alternativas": ["$9{,}0\\,\\text{m}$.", "$10\\,\\text{m}$.", "$30\\,\\text{m}$.", "$60\\,\\text{m}$.", "$90\\,\\text{m}$."],
        "gabarito": "C", # Wait, no period is given in text, but probably indicated in image. We will just leave it.
        "enunciado_adaptado": "\\imagem{Imagem5.png}\n\nO diagrama ilustra o movimento de uma onda do mar passando por uma boia, mostrando o tempo que leva para os picos passarem. As ondas viajam a 15 metros por segundo.\n\n\\textbf{Considerando os dados da imagem e da velocidade, qual é a distância de uma onda inteira (comprimento de onda)?}",
        "alternativas_adaptadas": ["10 m.", "30 m.", "90 m."],
        "gabarito_adaptado": "B",
        "imagem_adaptada": ""
    },
    {
        "id": get_id(),
        "tipo": "objetiva",
        "banca": "UPE",
        "ano": "0",
        "disciplina": "Física",
        "topico": "Ondulatória",
        "conteudo": "Ondas Eletromagnéticas",
        "assunto": "Frequência e Velocidade",
        "dificuldade": "medio",
        "enunciado": "A figura a seguir ilustra o movimento de uma onda eletromagnética que se propaga com velocidade de $72\\,\\text{km/h}$.\n\n\\imagem{Imagem6.png}\n\nDe acordo com a figura, podemos afirmar que a frequência, em Hz, dessa onda é:",
        "alternativas": ["500", "250", "2\\,000", "1\\,000", "3\\,600"],
        "gabarito": "A",
        "enunciado_adaptado": "\\imagem{Imagem6.png}\n\nO gráfico mostra uma onda viajando em uma velocidade de 72 km/h. Na régua do desenho, podemos ver o tamanho físico da onda.\n\n\\textbf{Com base nesses dados, quantas vezes a onda vibra por segundo (qual a sua frequência)?}",
        "alternativas_adaptadas": ["500 Hz.", "2\\,000 Hz.", "3\\,600 Hz."],
        "gabarito_adaptado": "A",
        "imagem_adaptada": ""
    },
    {
        "id": get_id(),
        "tipo": "discursiva",
        "banca": "UFPR",
        "ano": "0",
        "disciplina": "Física",
        "topico": "Ondulatória",
        "conteudo": "Propriedades das Ondas",
        "assunto": "Relação Comprimento e Período",
        "dificuldade": "medio",
        "enunciado": "A velocidade das ondas sonoras num dado meio vale $v$. Nesse meio, são produzidas duas ondas sonoras com comprimentos de onda $\\lambda_1$ e $\\lambda_2$, respectivamente, e com períodos $T_1$ e $T_2$, respectivamente. Determine a razão $T_1/T_2$ quando a relação entre os comprimentos de onda das duas ondas é tal que $\\lambda_1 = 5\\lambda_2$.",
        "alternativas": [],
        "gabarito": "5",
        "enunciado_adaptado": "Duas ondas sonoras viajam com a mesma velocidade em um meio. Sabe-se que a primeira onda tem um comprimento 5 vezes maior que o da segunda onda.\n\n\\textbf{Qual é a razão (proporção) entre o tempo do ciclo (período) da primeira e da segunda onda?}",
        "alternativas_adaptadas": [],
        "gabarito_adaptado": "5",
        "imagem_adaptada": ""
    },
    {
        "id": get_id(),
        "tipo": "discursiva",
        "banca": "UNIFESP",
        "ano": "0",
        "disciplina": "Física",
        "topico": "Cinemática",
        "conteudo": "Movimento Circular Uniforme",
        "assunto": "Composição de Movimentos",
        "dificuldade": "dificil",
        "enunciado": "Um avião, logo após a aterrissagem, está em movimento retilíneo sobre a pista horizontal, com sua hélice girando em uma frequência constante de 4 Hz.\n\nConsidere que, em um determinado intervalo de tempo, a velocidade escalar desse avião em relação ao solo é constante e igual a 2 m/s, que cada pá da hélice tem 1 m de comprimento e que $\\pi = 3$. Calcule\n\na) a distância, em metros, percorrida pelo avião enquanto sua hélice dá 12 voltas completas.\n\nb) o módulo da velocidade vetorial instantânea, em m/s, de um ponto da extremidade de uma das pás da hélice do avião em relação ao solo, em determinado instante desse intervalo.",
        "alternativas": [],
        "gabarito": "a) 6 m; b) 24,08 m/s",
        "enunciado_adaptado": "Um avião está andando na pista a $2\\,\\text{m/s}$ depois de pousar, e sua hélice gira 4 vezes por segundo. \n\n\\textbf{Sabendo que a hélice demora algum tempo para dar 12 voltas completas, qual a distância que o avião percorreu na pista durante essas 12 voltas da hélice?}",
        "alternativas_adaptadas": [],
        "gabarito_adaptado": "6 metros.",
        "imagem_adaptada": ""
    }
]

def format_alternatives(alts):
    letters = ['A', 'B', 'C', 'D', 'E']
    res = "\\begin{alternativas}\n"
    for idx, a in enumerate(alts):
        res += f"    \\alt{{{letters[idx]}}}{{{a}}}\n"
    res += "  \\end{alternativas}"
    return res

output = []
for q in questions:
    alts_tex = format_alternatives(q['alternativas']) if q['tipo'] == 'objetiva' else ""
    alts_ad_tex = format_alternatives(q['alternativas_adaptadas']) if q['tipo'] == 'objetiva' else ""
    
    q_tex = f"""\\begin{{questao}}{{{q['id']}}}
  \\meta{{tipo}}{{{q['tipo']}}}
  \\meta{{banca}}{{{q['banca']}}}
  \\meta{{ano}}{{{q['ano']}}}
  \\meta{{disciplina}}{{{q['disciplina']}}}
  \\meta{{topico}}{{{q['topico']}}}
  \\meta{{conteudo}}{{{q['conteudo']}}}
  \\meta{{assunto}}{{{q['assunto']}}}
  \\meta{{dificuldade}}{{{q['dificuldade']}}}

  \\enunciado{{
    {q['enunciado']}
  }}
"""
    if alts_tex:
        q_tex += f"\n  {alts_tex}\n"
    
    q_tex += f"\n  \\gabarito{{{q['gabarito']}}}\n\\end{{questao}}\n"

    diff_map = {"dificil": "medio", "medio": "facil", "facil": "facil"}
    ad_dif = diff_map[q['dificuldade']]

    q_ad_tex = f"""\\begin{{questao}}{{A-{q['id']}}}
  \\meta{{tipo}}{{{q['tipo']}}}
  \\meta{{banca}}{{{q['banca']}}}
  \\meta{{ano}}{{{q['ano']}}}
  \\meta{{disciplina}}{{{q['disciplina']}}}
  \\meta{{topico}}{{{q['topico']}}}
  \\meta{{conteudo}}{{{q['conteudo']}}}
  \\meta{{assunto}}{{{q['assunto']}}}
  \\meta{{dificuldade}}{{{ad_dif}}}

  \\enunciado{{
    {q['enunciado_adaptado']}
  }}
"""
    if alts_ad_tex:
        q_ad_tex += f"\n  {alts_ad_tex}\n"
    
    q_ad_tex += f"\n  \\gabarito{{{q['gabarito_adaptado']}}}\n\\end{{questao}}\n"
    
    output.append(q_tex)
    output.append(q_ad_tex)

with open('saida/questoes.tex', 'w', encoding='utf-8') as f:
    f.write("\n".join(output))
