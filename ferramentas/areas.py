"""Áreas públicas e o que cada esfera faz nelas.

Cada área trata de um assunto só. Quando um tema junta coisas diferentes (por
exemplo, "esporte e lazer"), ele vira duas áreas. As áreas são agrupadas em
eixos só para facilitar a navegação.

None = não é competência daquela esfera.
"""

EIXOS = [
    ("social", "Políticas sociais"),
    ("direitos", "Direitos e cidadania"),
    ("seguranca", "Segurança e justiça"),
    ("economia", "Economia, trabalho e produção"),
    ("infraestrutura", "Infraestrutura, transporte e energia"),
    ("cidades", "Cidades e moradia"),
    ("ambiente", "Meio ambiente"),
    ("tecnologia", "Ciência, tecnologia e comunicações"),
    ("financas", "Finanças públicas"),
    ("estado", "Estado e instituições"),
]


def _a(id, nome, eixo, federal, estadual, municipal):
    return dict(id=id, nome=nome, eixo=eixo, federal=federal, estadual=estadual, municipal=municipal)


AREAS = [
    # ---------------- Políticas sociais ----------------
    _a(
        "saude", "Saúde", "social",
        "Coordena o SUS, financia estados e municípios, compra vacinas e medicamentos estratégicos, "
        "regula planos de saúde (ANS) e a vigilância sanitária (Anvisa) e mantém hospitais federais e "
        "universitários.",
        "Hospitais regionais e de alta complexidade, hemocentros, laboratórios centrais, regulação de "
        "leitos, assistência farmacêutica especializada e apoio aos municípios.",
        "Atenção básica (UBS e Estratégia Saúde da Família), UPAs, vigilância epidemiológica e "
        "sanitária local, combate a endemias e saúde bucal e mental na rede municipal.",
    ),
    _a(
        "educacao", "Educação", "social",
        "Universidades e institutos federais, ensino superior (ProUni, Fies, Capes), Base Nacional "
        "Comum Curricular, Enem, complementação do Fundeb e programas de merenda (PNAE), livro "
        "didático e transporte escolar.",
        "Ensino médio, parte do ensino fundamental, ensino técnico e universidades estaduais e "
        "formação dos professores da rede.",
        "Creches, pré-escola e ensino fundamental, alfabetização, educação de jovens e adultos, "
        "merenda e transporte escolar.",
    ),
    _a(
        "assistencia-social", "Assistência social", "social",
        "Bolsa Família, Benefício de Prestação Continuada (BPC), Cadastro Único e cofinanciamento do "
        "SUAS.",
        "Cofinanciamento e apoio técnico aos municípios e serviços regionais de média e alta "
        "complexidade.",
        "CRAS e CREAS, abrigos, acompanhamento de famílias e inscrição no Cadastro Único.",
    ),
    _a(
        "previdencia", "Previdência social", "social",
        "INSS e Regime Geral de Previdência Social: regras de aposentadoria, pensões e benefícios, e "
        "normas gerais dos regimes próprios dos servidores.",
        "Regime próprio de previdência dos servidores do estado: regras locais, equilíbrio atuarial "
        "e gestão do fundo.",
        "Regime próprio de previdência dos servidores municipais, onde existir: gestão do instituto, "
        "equilíbrio atuarial e investimentos.",
    ),
    _a(
        "seguranca-alimentar", "Segurança alimentar", "social",
        "Sistema Nacional de Segurança Alimentar e Nutricional (Sisan), Programa de Aquisição de "
        "Alimentos (PAA), estoques públicos e combate à fome.",
        "Conselho e plano estaduais de segurança alimentar, restaurantes populares estaduais e "
        "compras públicas da agricultura familiar.",
        "Restaurantes populares, cozinhas comunitárias, bancos de alimentos e hortas comunitárias.",
    ),
    _a(
        "cultura", "Cultura", "social",
        "Lei Rouanet, Política Nacional Aldir Blanc, Ancine e museus e bibliotecas federais.",
        "Equipamentos culturais estaduais, editais e festivais.",
        "Centros culturais, bibliotecas, festas populares e editais locais.",
    ),
    _a(
        "patrimonio-cultural", "Patrimônio cultural", "social",
        "Tombamento e proteção do patrimônio material e imaterial de interesse nacional (Iphan) e "
        "sítios arqueológicos.",
        "Órgão estadual de patrimônio, tombamentos estaduais e restauro de bens do estado.",
        "Tombamento municipal, conservação de centros históricos e incentivos fiscais para imóveis "
        "protegidos.",
    ),
    _a(
        "esporte", "Esporte", "social",
        "Lei de Incentivo ao Esporte, Bolsa Atleta, esporte de alto rendimento, grandes eventos e "
        "programas nacionais de esporte educacional.",
        "Equipamentos e programas esportivos estaduais e jogos escolares.",
        "Quadras, ginásios, escolinhas esportivas, ligas e competições locais.",
    ),
    _a(
        "lazer", "Lazer", "social",
        "Programas nacionais de lazer e de atividade física para a população.",
        "Parques estaduais abertos ao público e programas regionais de lazer.",
        "Praças, parques urbanos, ruas de lazer, colônias de férias e atividades nos bairros.",
    ),
    # ---------------- Direitos e cidadania ----------------
    _a(
        "direitos-humanos", "Direitos humanos", "direitos",
        "Política nacional de direitos humanos, Disque 100, proteção a defensores de direitos humanos "
        "e combate à tortura e ao trabalho escravo.",
        "Programas estaduais de proteção (testemunhas, defensores de direitos humanos), comitês de "
        "combate à tortura e conselho estadual de direitos humanos.",
        "Centros de referência em direitos humanos, conselho municipal e educação em direitos.",
    ),
    _a(
        "mulheres", "Mulheres", "direitos",
        "Política nacional para as mulheres, Lei Maria da Penha, Ligue 180, Casa da Mulher Brasileira "
        "e igualdade salarial.",
        "Delegacias da mulher, patrulhas Maria da Penha, casas-abrigo e centros de referência "
        "estaduais.",
        "Centros de referência da mulher, casas-abrigo, rede de atendimento local e creches para mães "
        "que trabalham.",
    ),
    _a(
        "igualdade-racial", "Igualdade racial", "direitos",
        "Estatuto da Igualdade Racial, cotas no serviço público e nas universidades federais e "
        "combate ao racismo.",
        "Política estadual de igualdade racial, cotas nos concursos e universidades do estado e "
        "delegacias de crimes raciais.",
        "Coordenadoria de igualdade racial, cotas nos concursos municipais e ensino de história "
        "afro-brasileira na rede.",
    ),
    _a(
        "pessoas-com-deficiencia", "Pessoas com deficiência", "direitos",
        "Lei Brasileira de Inclusão, BPC, cotas de emprego e normas nacionais de acessibilidade.",
        "Centros de reabilitação, educação inclusiva na rede estadual e acessibilidade no transporte "
        "intermunicipal.",
        "Acessibilidade de calçadas, prédios e ônibus, transporte adaptado, educação inclusiva e "
        "atendimento na rede municipal.",
    ),
    _a(
        "pessoas-idosas", "Pessoas idosas", "direitos",
        "Estatuto da Pessoa Idosa, Fundo Nacional da Pessoa Idosa e política nacional de cuidados.",
        "Instituições de longa permanência, conselho estadual e gratuidade no transporte "
        "intermunicipal.",
        "Centros-dia e de convivência, cuidadores, atendimento domiciliar e conselho municipal.",
    ),
    _a(
        "criancas-e-adolescentes", "Crianças e adolescentes", "direitos",
        "Estatuto da Criança e do Adolescente (ECA), Marco Legal da Primeira Infância, Conanda e "
        "combate ao trabalho infantil e à violência sexual.",
        "Sistema socioeducativo (internação de adolescentes), conselho estadual e programas de "
        "proteção.",
        "Conselhos tutelares, acolhimento institucional e familiar, medidas socioeducativas em meio "
        "aberto e programas de primeira infância.",
    ),
    _a(
        "juventude", "Juventude", "direitos",
        "Estatuto da Juventude, ID Jovem e programas nacionais para jovens de 15 a 29 anos.",
        "Programas estaduais de juventude, primeiro emprego e conselho estadual.",
        "Centros de juventude, programas culturais e esportivos para jovens e conselho municipal.",
    ),
    _a(
        "populacao-lgbtqia", "População LGBTQIA+", "direitos",
        "Política nacional de direitos LGBTQIA+, combate à LGBTfobia (crime de racismo, por decisão "
        "do STF) e nome social no serviço público federal.",
        "Centros de referência estaduais, delegacias especializadas e nome social nos serviços do "
        "estado.",
        "Centros de cidadania LGBTQIA+, acolhimento de pessoas expulsas de casa e nome social nos "
        "serviços municipais.",
    ),
    _a(
        "populacao-em-situacao-de-rua", "População em situação de rua", "direitos",
        "Política nacional para a população em situação de rua e cofinanciamento dos serviços.",
        "Apoio aos municípios, vagas em serviços regionais e atendimento em saúde mental.",
        "Abordagem social, Centros Pop, abrigos e repúblicas, consultório na rua e moradia primeiro.",
    ),
    _a(
        "migrantes", "Migrantes", "direitos",
        "Lei de Migração, refúgio (Conare), documentação, acolhida humanitária e interiorização.",
        "Comitês estaduais para migrantes e refugiados e acesso aos serviços do estado.",
        "Centros de referência, acolhimento, ensino de português e acesso aos serviços municipais.",
    ),
    _a(
        "povos-indigenas", "Povos indígenas", "direitos",
        "Demarcação de terras indígenas, Funai, saúde indígena (Sesai) e proteção dos territórios.",
        "Educação escolar indígena e apoio às comunidades.",
        None,
    ),
    _a(
        "quilombolas", "Quilombolas", "direitos",
        "Certificação das comunidades (Fundação Palmares) e titulação dos territórios em terras da "
        "União (Incra).",
        "Titulação de territórios quilombolas em terras estaduais e educação escolar quilombola.",
        None,
    ),
    _a(
        "comunidades-tradicionais", "Comunidades tradicionais", "direitos",
        "Política nacional para povos e comunidades tradicionais (ribeirinhos, extrativistas, "
        "pescadores artesanais, ciganos, quebradeiras de coco, entre outros) e reservas "
        "extrativistas.",
        "Reconhecimento e regularização de territórios tradicionais em terras do estado.",
        None,
    ),
    _a(
        "participacao-social", "Participação social", "direitos",
        "Conselhos e conferências nacionais, consultas públicas e participação no Plano Plurianual.",
        "Conselhos e conferências estaduais e audiências públicas do orçamento.",
        "Orçamento participativo, conselhos municipais, audiências públicas e associações de bairro.",
    ),
    _a(
        "acesso-a-justica", "Acesso à justiça", "direitos",
        "Defensoria Pública da União e legislação processual.",
        "Defensoria Pública do estado e apoio a centros de conciliação e mediação.",
        "Assistência jurídica gratuita municipal, onde houver lei local, e núcleos de mediação de "
        "conflitos nos bairros.",
    ),
    # ---------------- Segurança e justiça ----------------
    _a(
        "seguranca-publica", "Segurança pública", "seguranca",
        "Polícia Federal, Polícia Rodoviária Federal, Força Nacional, controle de fronteiras, armas e "
        "crimes interestaduais e internacionais, Fundo Nacional de Segurança Pública e legislação "
        "penal.",
        "Polícia Militar, Polícia Civil, Corpo de Bombeiros e polícia científica. É o principal "
        "responsável pela segurança no dia a dia.",
        "Guarda municipal, videomonitoramento, ocupação de espaços públicos e prevenção da violência. "
        "O município não comanda polícia.",
    ),
    _a(
        "sistema-prisional", "Sistema prisional", "seguranca",
        "Presídios federais, Fundo Penitenciário Nacional, Lei de Execução Penal e penas "
        "alternativas.",
        "Presídios estaduais, vagas, ressocialização, trabalho e estudo dos presos e audiências de "
        "custódia.",
        "Apoio a egressos e vagas para penas de prestação de serviços à comunidade.",
    ),
    _a(
        "politica-sobre-drogas", "Política sobre drogas", "seguranca",
        "Lei de Drogas, Sistema Nacional de Políticas sobre Drogas (Sisnad), Fundo Nacional "
        "Antidrogas e repressão ao tráfico internacional.",
        "Prevenção, tratamento em parceria com a saúde e repressão ao tráfico pelas polícias do "
        "estado.",
        "Prevenção nas escolas, CAPS AD, redução de danos e reinserção social.",
    ),
    _a(
        "defesa-civil", "Defesa civil", "seguranca",
        "Sistema Nacional de Proteção e Defesa Civil, recursos para resposta e reconstrução após "
        "desastres e alertas e monitoramento (Cemaden).",
        "Defesa civil estadual, Corpo de Bombeiros e apoio aos municípios em desastres.",
        "Defesa civil municipal, mapeamento de áreas de risco, planos de contingência, alertas e "
        "abrigos.",
    ),
    _a(
        "defesa-do-consumidor", "Defesa do consumidor", "seguranca",
        "Código de Defesa do Consumidor, Secretaria Nacional do Consumidor e plataforma "
        "consumidor.gov.br.",
        "Procon estadual, fiscalização e mediação de conflitos de consumo.",
        "Procon municipal, fiscalização local e orientação ao consumidor.",
    ),
    # ---------------- Economia, trabalho e produção ----------------
    _a(
        "desenvolvimento-economico", "Desenvolvimento econômico", "economia",
        "Política de desenvolvimento produtivo, BNDES e bancos públicos federais e crédito para "
        "investimento.",
        "Atração de investimentos, agências e bancos de fomento estaduais e incentivos fiscais "
        "dentro das regras da reforma tributária.",
        "Atração de empresas, distritos industriais e ambiente de negócios local.",
    ),
    _a(
        "desenvolvimento-regional", "Desenvolvimento regional", "economia",
        "Sudene, Sudam e Sudeco, fundos constitucionais de financiamento (FNE, FNO, FCO) e política "
        "nacional de desenvolvimento regional.",
        "Planejamento regional dentro do estado e redução de desigualdades entre suas regiões.",
        None,
    ),
    _a(
        "industria", "Indústria", "economia",
        "Política industrial (Nova Indústria Brasil), conteúdo local, financiamento e normas técnicas "
        "(Inmetro).",
        "Polos industriais, incentivos e qualificação de mão de obra para a indústria.",
        "Distritos industriais e licenciamento de atividades no município.",
    ),
    _a(
        "comercio", "Comércio", "economia",
        "Regras gerais do comércio e da concorrência no mercado interno.",
        "Apoio ao comércio regional e simplificação de registros na junta comercial.",
        "Alvarás, horários de funcionamento, feiras, mercados municipais, comércio de rua e centros "
        "comerciais.",
    ),
    _a(
        "comercio-exterior", "Comércio exterior", "economia",
        "Tarifas de importação, acordos comerciais, defesa comercial, Camex e promoção de "
        "exportações (ApexBrasil).",
        "Agências estaduais de promoção de exportações e atração de investimento estrangeiro.",
        None,
    ),
    _a(
        "empreendedorismo", "Empreendedorismo", "economia",
        "Simples Nacional, MEI, Estatuto da Microempresa e crédito para pequenos negócios "
        "(Pronampe).",
        "Crédito estadual para pequenos negócios, apoio do Sebrae e compras públicas de pequenas "
        "empresas.",
        "Sala do Empreendedor, licenças rápidas, compras públicas de pequenos negócios locais e "
        "microcrédito.",
    ),
    _a(
        "economia-solidaria", "Economia solidária", "economia",
        "Política nacional de economia solidária, cooperativas e finanças solidárias.",
        "Apoio a cooperativas, incubadoras e redes de comercialização.",
        "Bancos comunitários, moedas sociais, feiras de economia solidária e apoio a cooperativas de "
        "catadores.",
    ),
    _a(
        "defesa-da-concorrencia", "Defesa da concorrência", "economia",
        "Cade, controle de fusões e combate a cartéis e abuso de poder econômico.",
        None,
        None,
    ),
    _a(
        "trabalho", "Trabalho", "economia",
        "Legislação trabalhista, fiscalização do trabalho, combate ao trabalho escravo e infantil e "
        "saúde e segurança no trabalho.",
        "Comissões estaduais de combate ao trabalho escravo e saúde do trabalhador na rede estadual.",
        "Centros de referência em saúde do trabalhador e condições de trabalho nos serviços "
        "contratados pela prefeitura.",
    ),
    _a(
        "emprego", "Emprego", "economia",
        "Seguro-desemprego, FGTS, Sine e programas nacionais de qualificação profissional.",
        "Postos do Sine, qualificação profissional e programas de primeiro emprego.",
        "Intermediação de mão de obra, qualificação local e frentes de trabalho.",
    ),
    _a(
        "renda", "Renda", "economia",
        "Salário mínimo, abono salarial e programas nacionais de transferência de renda.",
        "Programas estaduais de transferência de renda complementares aos federais.",
        "Programas municipais de renda básica e complementação de renda.",
    ),
    _a(
        "turismo", "Turismo", "economia",
        "Embratur, promoção internacional, cadastro de prestadores (Cadastur) e financiamento "
        "(Fungetur).",
        "Promoção do estado, rotas regionais e infraestrutura turística.",
        "Calendário de eventos, sinalização turística e conservação dos atrativos locais.",
    ),
    _a(
        "agricultura", "Agricultura", "economia",
        "Plano Safra, crédito e seguro rural, Embrapa, zoneamento agrícola e defesa vegetal.",
        "Assistência técnica e extensão rural, defesa sanitária vegetal e pesquisa agropecuária "
        "estadual.",
        "Estradas vicinais, patrulha mecanizada, hortas urbanas e apoio a produtores locais.",
    ),
    _a(
        "agricultura-familiar", "Agricultura familiar", "economia",
        "Pronaf, Garantia-Safra, assistência técnica (Anater) e compras públicas da agricultura "
        "familiar.",
        "Extensão rural para agricultores familiares, crédito e apoio a cooperativas.",
        "Compra da agricultura familiar para a merenda (no mínimo 30% do PNAE), feiras do produtor e "
        "apoio a cooperativas.",
    ),
    _a(
        "pecuaria", "Pecuária", "economia",
        "Defesa sanitária animal, controle de doenças (febre aftosa, gripe aviária) e inspeção "
        "federal de produtos de origem animal.",
        "Agência estadual de defesa agropecuária, controle do trânsito de animais e inspeção "
        "estadual.",
        "Serviço de inspeção municipal de produtos de origem animal e apoio a pequenos criadores.",
    ),
    _a(
        "pesca", "Pesca", "economia",
        "Ordenamento da pesca e da aquicultura, seguro-defeso do pescador artesanal e registro de "
        "pescadores.",
        "Apoio à aquicultura, extensão pesqueira e licenciamento de criadouros.",
        "Terminais pesqueiros, mercados de peixe e apoio às colônias de pescadores.",
    ),
    _a(
        "abastecimento", "Abastecimento", "economia",
        "Conab, estoques reguladores, garantia de preços mínimos e Ceasas federais.",
        "Centrais de abastecimento (Ceasas) estaduais e logística de alimentos.",
        "Mercados municipais, sacolões e varejões populares.",
    ),
    _a(
        "reforma-agraria", "Reforma agrária", "economia",
        "Desapropriação de terras improdutivas, assentamentos e crédito fundiário (Incra).",
        "Institutos estaduais de terras, regularização de terras devolutas e apoio aos "
        "assentamentos.",
        "Estradas, escolas e postos de saúde que atendem os assentamentos do município.",
    ),
    # ---------------- Infraestrutura, transporte e energia ----------------
    _a(
        "obras-publicas", "Obras públicas", "infraestrutura",
        "Grandes obras de interesse nacional, transferências para obras de estados e municípios e "
        "parcerias público-privadas federais.",
        "Obras estaduais (estradas, prédios, barragens), parcerias público-privadas estaduais e apoio "
        "a obras municipais.",
        "Pavimentação, pontes, prédios públicos e contratos de obras do município.",
    ),
    _a(
        "rodovias", "Rodovias", "infraestrutura",
        "Rodovias federais (DNIT), concessões rodoviárias e Polícia Rodoviária Federal.",
        "Rodovias estaduais, departamento de estradas e concessões estaduais.",
        "Estradas municipais e vicinais.",
    ),
    _a(
        "ferrovias", "Ferrovias", "infraestrutura",
        "Malha ferroviária federal, concessões e autorizações de ferrovias (ANTT).",
        "Ferrovias estaduais, onde o estado as autoriza ou constrói.",
        None,
    ),
    _a(
        "hidrovias", "Hidrovias", "infraestrutura",
        "Hidrovias federais, dragagem e regulação da navegação interior (Antaq).",
        "Travessias e transporte hidroviário intermunicipal, como balsas e lanchas.",
        "Transporte hidroviário urbano e travessias dentro do município.",
    ),
    _a(
        "portos", "Portos", "infraestrutura",
        "Portos públicos, arrendamentos e terminais privados (Antaq e autoridades portuárias).",
        "Portos delegados ao estado pela União.",
        "Acesso viário ao porto e ordenamento do seu entorno urbano.",
    ),
    _a(
        "aeroportos", "Aeroportos", "infraestrutura",
        "Aviação civil (Anac), concessões de aeroportos e controle do espaço aéreo.",
        "Aeroportos regionais delegados ou mantidos pelo estado.",
        "Aeródromos municipais e acesso viário aos aeroportos.",
    ),
    _a(
        "transporte-publico", "Transporte público", "infraestrutura",
        "Financiamento de sistemas de transporte coletivo, marco legal do transporte público e "
        "transporte interestadual de passageiros.",
        "Transporte intermunicipal e metropolitano (metrô, trens, ônibus).",
        "Ônibus urbanos, tarifa, integração, corredores e faixas exclusivas.",
    ),
    _a(
        "transito", "Trânsito", "infraestrutura",
        "Código de Trânsito, Senatran, Contran e habilitação (normas nacionais).",
        "Detran: habilitação, licenciamento de veículos e fiscalização.",
        "Sinalização, semáforos, fiscalização de trânsito nas vias municipais, estacionamento, táxi e "
        "transporte por aplicativo.",
    ),
    _a(
        "mobilidade-ativa", "Mobilidade ativa", "infraestrutura",
        "Política nacional de mobilidade urbana (Lei 12.587/2012) e financiamento de ciclovias e "
        "calçadas.",
        "Ciclovias e acostamentos seguros nas rodovias estaduais e integração da bicicleta ao "
        "transporte metropolitano.",
        "Calçadas, ciclovias, bicicletas compartilhadas e travessias seguras para pedestres.",
    ),
    _a(
        "energia", "Energia", "infraestrutura",
        "Setor elétrico (Aneel, ONS), geração e transmissão, transição energética e tarifa social de "
        "energia.",
        "Incentivo a energia solar e eólica no estado e licenciamento de usinas.",
        "Eficiência energética e geração solar nos prédios públicos.",
    ),
    _a(
        "combustiveis", "Combustíveis", "infraestrutura",
        "Petróleo, gás natural e biocombustíveis (ANP), Petrobras, royalties e política de preços.",
        "Distribuição de gás canalizado e incentivo à produção de biocombustíveis no estado.",
        None,
    ),
    _a(
        "mineracao", "Mineração", "infraestrutura",
        "Outorga e fiscalização da mineração (ANM), segurança de barragens e royalties (CFEM).",
        "Licenciamento ambiental de minas e fiscalização de barragens em parceria com a União.",
        "Uso dos royalties de mineração (CFEM) recebidos pelo município e controle do impacto local.",
    ),
    _a(
        "iluminacao-publica", "Iluminação pública", "infraestrutura",
        None,
        None,
        "Instalação, manutenção e troca para LED da iluminação das vias, financiadas pela "
        "contribuição do art. 149-A da Constituição.",
    ),
    # ---------------- Cidades e moradia ----------------
    _a(
        "habitacao", "Habitação", "cidades",
        "Programas nacionais de moradia (Minha Casa, Minha Vida) e financiamento habitacional.",
        "Companhias estaduais de habitação, programas estaduais e contrapartidas aos programas "
        "federais.",
        "Cadastro e seleção das famílias, terrenos, urbanização de favelas e aluguel social.",
    ),
    _a(
        "regularizacao-fundiaria", "Regularização fundiária", "cidades",
        "Lei da Reurb (13.465/2017) e regularização em terras da União.",
        "Regularização em terras do estado e apoio técnico aos municípios.",
        "Reurb: levantamento dos núcleos informais, titulação das famílias e obras de infraestrutura.",
    ),
    _a(
        "planejamento-urbano", "Planejamento urbano", "cidades",
        "Estatuto da Cidade, política nacional de desenvolvimento urbano e financiamento.",
        "Planejamento das regiões metropolitanas e aglomerações urbanas.",
        "Plano diretor, zoneamento e uso do solo, licenciamento de obras e instrumentos do Estatuto "
        "da Cidade.",
    ),
    _a(
        "saneamento", "Saneamento básico", "cidades",
        "Marco legal do saneamento, normas de referência (ANA), financiamento (Caixa, BNDES) e metas "
        "nacionais de universalização.",
        "Companhias estaduais de saneamento, prestação regionalizada e saneamento nas regiões "
        "metropolitanas.",
        "É o titular do serviço de água, esgoto e drenagem. Presta diretamente ou contrata e faz o "
        "plano municipal de saneamento.",
    ),
    _a(
        "zeladoria", "Zeladoria urbana", "cidades",
        None,
        None,
        "Tapa-buraco, poda de árvores, capina, limpeza de bocas de lobo e manutenção de praças e "
        "calçadas públicas.",
    ),
    # ---------------- Meio ambiente ----------------
    _a(
        "meio-ambiente", "Meio ambiente", "ambiente",
        "Política nacional de meio ambiente, Ibama, licenciamento de grandes empreendimentos e "
        "controle da poluição.",
        "Órgão ambiental estadual, licenciamento e fiscalização.",
        "Licenciamento de impacto local, fiscalização, arborização e educação ambiental.",
    ),
    _a(
        "mudanca-do-clima", "Mudança do clima", "ambiente",
        "Política Nacional sobre Mudança do Clima, metas do Acordo de Paris, mercado de carbono e "
        "Fundo Clima.",
        "Planos estaduais de clima, inventário de emissões e adaptação.",
        "Plano municipal de adaptação e redução de emissões, ilhas de calor e arborização.",
    ),
    _a(
        "florestas", "Florestas", "ambiente",
        "Código Florestal, combate ao desmatamento, Cadastro Ambiental Rural (CAR) e concessões "
        "florestais.",
        "Validação do CAR, regularização ambiental de imóveis rurais e combate a queimadas.",
        "Áreas verdes, recomposição de matas ciliares e brigadas de incêndio locais.",
    ),
    _a(
        "biodiversidade", "Biodiversidade", "ambiente",
        "Unidades de conservação federais (ICMBio), espécies ameaçadas e patrimônio genético.",
        "Unidades de conservação estaduais e proteção da fauna e flora do estado.",
        "Parques naturais municipais e corredores ecológicos urbanos.",
    ),
    _a(
        "recursos-hidricos", "Recursos hídricos", "ambiente",
        "Política Nacional de Recursos Hídricos, ANA, rios federais, outorgas e segurança hídrica.",
        "Gestão dos rios estaduais, outorgas, comitês de bacia e barragens.",
        "Proteção de nascentes e mananciais e participação nos comitês de bacia.",
    ),
    _a(
        "residuos-solidos", "Resíduos sólidos", "ambiente",
        "Política Nacional de Resíduos Sólidos, logística reversa e fim dos lixões.",
        "Plano estadual de resíduos e apoio a consórcios intermunicipais e aterros regionais.",
        "Coleta de lixo e coleta seletiva, aterro sanitário, reciclagem e contratação de "
        "cooperativas de catadores.",
    ),
    _a(
        "protecao-animal", "Proteção animal", "ambiente",
        "Lei de crimes ambientais e de maus-tratos a animais e controle de zoonoses em âmbito "
        "nacional.",
        "Delegacias de proteção animal e fiscalização de maus-tratos.",
        "Castração, centros de controle de zoonoses, adoção e hospitais veterinários públicos.",
    ),
    # ---------------- Ciência, tecnologia e comunicações ----------------
    _a(
        "ciencia", "Ciência", "tecnologia",
        "CNPq, Capes, institutos de pesquisa federais e Fundo Nacional de Desenvolvimento Científico "
        "e Tecnológico (FNDCT).",
        "Fundação de amparo à pesquisa e universidades estaduais.",
        "Divulgação científica, museus de ciência e feiras escolares.",
    ),
    _a(
        "inovacao", "Inovação", "tecnologia",
        "Marco Legal da Inovação e das Startups, Finep, Embrapii e incentivos fiscais (Lei do Bem).",
        "Parques tecnológicos, incubadoras e lei estadual de inovação.",
        "Apoio a startups e empresas inovadoras locais e compras públicas de inovação.",
    ),
    _a(
        "inclusao-digital", "Inclusão digital", "tecnologia",
        "Conectividade de escolas e regiões sem internet (Fust) e programas nacionais de inclusão "
        "digital.",
        "Redes estaduais de conectividade e internet nas escolas estaduais.",
        "Wi-fi público, telecentros e conexão das escolas e unidades de saúde municipais.",
    ),
    _a(
        "telecomunicacoes", "Telecomunicações", "tecnologia",
        "Telefonia e internet (Anatel), leilões de frequência e metas de cobertura.",
        None,
        "Licenciamento de antenas e redes no espaço urbano (Lei Geral de Antenas, Lei 13.116/2015).",
    ),
    _a(
        "radiodifusao", "Radiodifusão", "tecnologia",
        "Concessões de rádio e TV e autorização de rádios comunitárias.",
        None,
        None,
    ),
    _a(
        "comunicacao-publica", "Comunicação pública", "tecnologia",
        "Empresa Brasil de Comunicação (EBC), publicidade oficial e comunicação do governo federal.",
        "TVs e rádios educativas do estado e publicidade oficial.",
        "Publicidade oficial e canais de informação da prefeitura.",
    ),
    _a(
        "servico-postal", "Serviço postal", "tecnologia",
        "Correios e universalização do serviço postal.",
        None,
        None,
    ),
    # ---------------- Finanças públicas ----------------
    _a(
        "politica-economica", "Política econômica", "financas",
        "Política fiscal, regras fiscais (arcabouço fiscal) e crédito público. A política monetária é "
        "do Banco Central, que é autônomo.",
        None,
        None,
    ),
    _a(
        "orcamento-publico", "Orçamento público", "financas",
        "Plano Plurianual, Lei de Diretrizes Orçamentárias e Lei Orçamentária Anual da União e "
        "repasses aos estados e municípios (FPE, FPM).",
        "PPA, LDO e LOA do estado, vinculações constitucionais e repasses aos municípios.",
        "PPA, LDO e LOA do município e aplicação dos mínimos em saúde e educação.",
    ),
    _a(
        "tributos", "Tributos", "financas",
        "Tributos federais (Imposto de Renda, CBS, IPI e contribuições) e regras gerais da reforma "
        "tributária.",
        "ICMS (em transição para o IBS), IPVA e ITCMD.",
        "IPTU, ISS (em transição para o IBS), ITBI e taxas.",
    ),
    _a(
        "divida-publica", "Dívida pública", "financas",
        "Dívida pública federal (Tesouro Nacional) e limites de endividamento propostos ao Senado.",
        "Dívida do estado, renegociação com a União e operações de crédito.",
        "Dívida do município e operações de crédito, dentro dos limites do Senado.",
    ),
    # ---------------- Estado e instituições ----------------
    _a(
        "gestao-publica", "Gestão pública", "estado",
        "Organização dos ministérios, planejamento e avaliação de políticas públicas.",
        "Organização das secretarias, planejamento e metas do governo do estado.",
        "Organização das secretarias, planejamento e metas da prefeitura.",
    ),
    _a(
        "servidores-publicos", "Servidores públicos", "estado",
        "Servidores federais: concursos, carreiras, salários e avaliação de desempenho.",
        "Servidores do estado: concursos, carreiras, salários e avaliação de desempenho.",
        "Servidores municipais: concursos, carreiras, salários e avaliação de desempenho.",
    ),
    _a(
        "compras-publicas", "Compras públicas", "estado",
        "Lei de Licitações (14.133/2021), Portal Nacional de Contratações Públicas e compras "
        "federais.",
        "Licitações, contratos e compras centralizadas do estado.",
        "Licitações, contratos e compras da prefeitura.",
    ),
    _a(
        "transparencia", "Transparência", "estado",
        "Lei de Acesso à Informação, Portal da Transparência e dados abertos federais.",
        "Portal da transparência do estado, dados abertos e serviço de informação ao cidadão.",
        "Portal da transparência do município, dados abertos e serviço de informação ao cidadão.",
    ),
    _a(
        "combate-a-corrupcao", "Combate à corrupção", "estado",
        "Controladoria-Geral da União, Lei Anticorrupção, acordos de leniência e integridade.",
        "Controladoria do estado, corregedoria e programas de integridade.",
        "Controladoria e corregedoria municipais e programas de integridade.",
    ),
    _a(
        "governo-digital", "Governo digital", "estado",
        "Gov.br, identidade digital, serviços públicos digitais e proteção de dados no governo.",
        "Serviços digitais do estado e integração ao gov.br.",
        "Serviços digitais da prefeitura, agendamento online e protocolo eletrônico.",
    ),
    _a(
        "atendimento-ao-cidadao", "Atendimento ao cidadão", "estado",
        "Ouvidoria-Geral da União e padrões de atendimento dos órgãos federais.",
        "Centrais de atendimento (tipo Poupatempo), ouvidoria e carta de serviços.",
        "Central de atendimento, telefone 156, ouvidoria e carta de serviços.",
    ),
    _a(
        "cooperacao-federativa", "Cooperação federativa", "estado",
        "Transferências voluntárias, convênios e relação com estados e municípios.",
        "Convênios com municípios e apoio a consórcios intermunicipais.",
        "Consórcios intermunicipais e convênios com o estado e a União.",
    ),
    _a(
        "defesa-nacional", "Defesa nacional", "estado",
        "Forças Armadas, indústria de defesa e proteção das fronteiras, do mar e do espaço aéreo.",
        None,
        None,
    ),
    _a(
        "relacoes-exteriores", "Relações exteriores", "estado",
        "Política externa, diplomacia, acordos internacionais, Mercosul e atendimento a brasileiros "
        "no exterior.",
        None,
        None,
    ),
]
