"""
Rozsiahla databáza slovenských firiem pre IČO lookup.
Obsahuje najväčšie a najznámejšie slovenské spoločnosti.
"""

SLOVAK_COMPANIES = {
    # ==================== BANKY ====================
    '35697270': {
        'name': 'Slovenská sporiteľňa, a.s.',
        'street': 'Tomášikova 48',
        'city': 'Bratislava',
        'zip_code': '83237',
        'ico': '35697270',
        'dic': '2020417809',
        'ic_dph': 'SK2020417809',
        'legal_form': 'a.s.'
    },
    '31340890': {
        'name': 'Tatra banka, a.s.',
        'street': 'Hodžovo námestie 3',
        'city': 'Bratislava',
        'zip_code': '81106',
        'ico': '31340890',
        'dic': '2020408522',
        'ic_dph': 'SK2020408522',
        'legal_form': 'a.s.'
    },
    '00151653': {
        'name': 'Všeobecná úverová banka, a.s.',
        'street': 'Mlynské nivy 1',
        'city': 'Bratislava',
        'zip_code': '82990',
        'ico': '00151653',
        'dic': '2020411811',
        'ic_dph': 'SK2020411811',
        'legal_form': 'a.s.'
    },
    '31575951': {
        'name': 'Československá obchodná banka, a.s.',
        'street': 'Žižkova 11',
        'city': 'Bratislava',
        'zip_code': '81102',
        'ico': '31575951',
        'dic': '2020408309',
        'ic_dph': 'SK2020408309',
        'legal_form': 'a.s.'
    },
    '35715324': {
        'name': 'mBank S.A., pobočka zahraničnej banky',
        'street': 'Štúrova 8',
        'city': 'Bratislava',
        'zip_code': '81102',
        'ico': '35715324',
        'dic': '2020270817',
        'ic_dph': 'SK2020270817',
        'legal_form': 'pobočka'
    },
    '36869783': {
        'name': 'Fio banka, a.s., pobočka zahraničnej banky',
        'street': 'Nám. SNP 21',
        'city': 'Bratislava',
        'zip_code': '81101',
        'ico': '36869783',
        'dic': '4020184041',
        'ic_dph': '',
        'legal_form': 'pobočka'
    },
    '17321123': {
        'name': 'Prima banka Slovensko, a.s.',
        'street': 'Hodžova 11',
        'city': 'Žilina',
        'zip_code': '01011',
        'ico': '17321123',
        'dic': '2020400148',
        'ic_dph': '',
        'legal_form': 'a.s.'
    },
    '35728515': {
        'name': 'UniCredit Bank Czech Republic and Slovakia, a.s.',
        'street': 'Šancová 1/A',
        'city': 'Bratislava',
        'zip_code': '81333',
        'ico': '35728515',
        'dic': '4020252279',
        'ic_dph': 'SK4020252279',
        'legal_form': 'a.s.'
    },
    
    # ==================== TELEKOMUNIKÁCIE ====================
    '31322832': {
        'name': 'Slovak Telekom, a.s.',
        'street': 'Bajkalská 28',
        'city': 'Bratislava',
        'zip_code': '81762',
        'ico': '31322832',
        'dic': '2020270687',
        'ic_dph': 'SK2020270687',
        'legal_form': 'a.s.'
    },
    '35763469': {
        'name': 'Orange Slovensko, a.s.',
        'street': 'Metodova 8',
        'city': 'Bratislava',
        'zip_code': '82108',
        'ico': '35763469',
        'dic': '2020310578',
        'ic_dph': 'SK2020310578',
        'legal_form': 'a.s.'
    },
    '35840773': {
        'name': 'O2 Slovakia, s.r.o.',
        'street': 'Einsteinova 24',
        'city': 'Bratislava',
        'zip_code': '85101',
        'ico': '35840773',
        'dic': '2020216748',
        'ic_dph': 'SK2020216748',
        'legal_form': 's.r.o.'
    },
    '47259116': {
        'name': 'SWAN, a.s.',
        'street': 'Borská 6',
        'city': 'Bratislava',
        'zip_code': '84104',
        'ico': '47259116',
        'dic': '2023844966',
        'ic_dph': 'SK2023844966',
        'legal_form': 'a.s.'
    },
    '35954612': {
        'name': '4ka, s.r.o.',
        'street': 'Moldavská cesta 8/A',
        'city': 'Košice',
        'zip_code': '04011',
        'ico': '35954612',
        'dic': '2022046389',
        'ic_dph': 'SK2022046389',
        'legal_form': 's.r.o.'
    },
    
    # ==================== ENERGIE ====================
    '35823551': {
        'name': 'Slovenský plynárenský priemysel, a.s.',
        'street': 'Mlynské nivy 44/a',
        'city': 'Bratislava',
        'zip_code': '82511',
        'ico': '35823551',
        'dic': '2020259802',
        'ic_dph': 'SK2020259802',
        'legal_form': 'a.s.'
    },
    '35829052': {
        'name': 'Západoslovenská energetika, a.s.',
        'street': 'Čulenova 6',
        'city': 'Bratislava',
        'zip_code': '81647',
        'ico': '35829052',
        'dic': '2020269333',
        'ic_dph': 'SK2020269333',
        'legal_form': 'a.s.'
    },
    '36211541': {
        'name': 'Stredoslovenská energetika, a.s.',
        'street': 'Pri Rajčianke 8591/4B',
        'city': 'Žilina',
        'zip_code': '01047',
        'ico': '36211541',
        'dic': '2020002654',
        'ic_dph': 'SK2020002654',
        'legal_form': 'a.s.'
    },
    '36599361': {
        'name': 'Východoslovenská energetika Holding a.s.',
        'street': 'Mlynská 31',
        'city': 'Košice',
        'zip_code': '04291',
        'ico': '36599361',
        'dic': '2022084033',
        'ic_dph': 'SK2022084033',
        'legal_form': 'a.s.'
    },
    '35822350': {
        'name': 'Slovenské elektrárne, a.s.',
        'street': 'Mlynské nivy 47',
        'city': 'Bratislava',
        'zip_code': '82109',
        'ico': '35822350',
        'dic': '2020259810',
        'ic_dph': 'SK2020259810',
        'legal_form': 'a.s.'
    },
    '36361518': {
        'name': 'Západoslovenská distribučná, a.s.',
        'street': 'Čulenova 6',
        'city': 'Bratislava',
        'zip_code': '81647',
        'ico': '36361518',
        'dic': '2022189048',
        'ic_dph': 'SK2022189048',
        'legal_form': 'a.s.'
    },
    '36442151': {
        'name': 'Stredoslovenská distribučná, a.s.',
        'street': 'Pri Rajčianke 2927/8',
        'city': 'Žilina',
        'zip_code': '01047',
        'ico': '36442151',
        'dic': '2022187660',
        'ic_dph': 'SK2022187660',
        'legal_form': 'a.s.'
    },
    '36599191': {
        'name': 'Východoslovenská distribučná, a.s.',
        'street': 'Mlynská 31',
        'city': 'Košice',
        'zip_code': '04291',
        'ico': '36599191',
        'dic': '2022086768',
        'ic_dph': 'SK2022086768',
        'legal_form': 'a.s.'
    },
    '35937874': {
        'name': 'Bratislavská teplárenská, a.s.',
        'street': 'Turbínová 3',
        'city': 'Bratislava',
        'zip_code': '82964',
        'ico': '35937874',
        'dic': '2022127706',
        'ic_dph': 'SK2022127706',
        'legal_form': 'a.s.'
    },
    '00681709': {
        'name': 'Slovenský vodohospodársky podnik, š.p.',
        'street': 'Martinská 49',
        'city': 'Banská Štiavnica',
        'zip_code': '96901',
        'ico': '00681709',
        'dic': '2020451067',
        'ic_dph': '',
        'legal_form': 'š.p.'
    },
    '35850370': {
        'name': 'Bratislavská vodárenská spoločnosť, a.s.',
        'street': 'Prešovská 48',
        'city': 'Bratislava',
        'zip_code': '82602',
        'ico': '35850370',
        'dic': '2021268757',
        'ic_dph': 'SK2021268757',
        'legal_form': 'a.s.'
    },
    
    # ==================== OBCHODNÉ REŤAZCE ====================
    '35790164': {
        'name': 'TESCO STORES SR, a.s.',
        'street': 'Kamenné námestie 1/A',
        'city': 'Bratislava',
        'zip_code': '81599',
        'ico': '35790164',
        'dic': '2020269680',
        'ic_dph': 'SK2020269680',
        'legal_form': 'a.s.'
    },
    '35722428': {
        'name': 'Kaufland Slovenská republika v.o.s.',
        'street': 'Trnavská cesta 41/A',
        'city': 'Bratislava',
        'zip_code': '83104',
        'ico': '35722428',
        'dic': '2020263940',
        'ic_dph': 'SK2020263940',
        'legal_form': 'v.o.s.'
    },
    '35763132': {
        'name': 'Lidl Slovenská republika, v.o.s.',
        'street': 'Ružinovská 1E',
        'city': 'Bratislava',
        'zip_code': '82102',
        'ico': '35763132',
        'dic': '2020256188',
        'ic_dph': 'SK2020256188',
        'legal_form': 'v.o.s.'
    },
    '31347037': {
        'name': 'BILLA s.r.o.',
        'street': 'Bajkalská 19/A',
        'city': 'Bratislava',
        'zip_code': '82109',
        'ico': '31347037',
        'dic': '2020334633',
        'ic_dph': 'SK2020334633',
        'legal_form': 's.r.o.'
    },
    '34115609': {
        'name': 'CBA Slovakia, a.s.',
        'street': 'Galvaniho 7/D',
        'city': 'Bratislava',
        'zip_code': '82104',
        'ico': '34115609',
        'dic': '2020336633',
        'ic_dph': 'SK2020336633',
        'legal_form': 'a.s.'
    },
    '35757531': {
        'name': 'METRO Cash & Carry SR s.r.o.',
        'street': 'Senecká cesta 1881',
        'city': 'Ivanka pri Dunaji',
        'zip_code': '90028',
        'ico': '35757531',
        'dic': '2020256006',
        'ic_dph': 'SK2020256006',
        'legal_form': 's.r.o.'
    },
    '35867761': {
        'name': 'COOP Jednota Slovensko, s.d.',
        'street': 'Bajkalská 25',
        'city': 'Bratislava',
        'zip_code': '82718',
        'ico': '35867761',
        'dic': '2021716505',
        'ic_dph': 'SK2021716505',
        'legal_form': 's.d.'
    },
    '36241920': {
        'name': 'NAY a.s.',
        'street': 'Tuhovská 5',
        'city': 'Bratislava',
        'zip_code': '83106',
        'ico': '36241920',
        'dic': '2020095533',
        'ic_dph': 'SK2020095533',
        'legal_form': 'a.s.'
    },
    '36400653': {
        'name': 'DM drogerie markt s.r.o.',
        'street': 'Na pántoch 18',
        'city': 'Bratislava',
        'zip_code': '83106',
        'ico': '36400653',
        'dic': '2020078413',
        'ic_dph': 'SK2020078413',
        'legal_form': 's.r.o.'
    },
    '31361358': {
        'name': 'IKEA Bratislava, s.r.o.',
        'street': 'Ivanská cesta 18',
        'city': 'Bratislava',
        'zip_code': '82104',
        'ico': '31361358',
        'dic': '2020333814',
        'ic_dph': 'SK2020333814',
        'legal_form': 's.r.o.'
    },
    '35733870': {
        'name': 'Hornbach-Baumarkt SK spol. s r.o.',
        'street': 'Cesta na Senec 2',
        'city': 'Bratislava',
        'zip_code': '82104',
        'ico': '35733870',
        'dic': '2020271090',
        'ic_dph': 'SK2020271090',
        'legal_form': 's.r.o.'
    },
    '31356885': {
        'name': 'OBI Slovensko s.r.o.',
        'street': 'Vajnorská 100/B',
        'city': 'Bratislava',
        'zip_code': '83104',
        'ico': '31356885',
        'dic': '2020339594',
        'ic_dph': 'SK2020339594',
        'legal_form': 's.r.o.'
    },
    
    # ==================== IT & TECH ====================
    '35760419': {
        'name': 'ESET, spol. s r.o.',
        'street': 'Einsteinova 24',
        'city': 'Bratislava',
        'zip_code': '85101',
        'ico': '35760419',
        'dic': '2020254918',
        'ic_dph': 'SK2020254918',
        'legal_form': 's.r.o.'
    },
    '36237337': {
        'name': 'Asseco Central Europe, a.s.',
        'street': 'Trenčianska 56/A',
        'city': 'Bratislava',
        'zip_code': '82109',
        'ico': '36237337',
        'dic': '2020001513',
        'ic_dph': 'SK2020001513',
        'legal_form': 'a.s.'
    },
    '31331131': {
        'name': 'PosAm, spol. s r.o.',
        'street': 'Odborárska 52',
        'city': 'Bratislava',
        'zip_code': '83102',
        'ico': '31331131',
        'dic': '2020342792',
        'ic_dph': 'SK2020342792',
        'legal_form': 's.r.o.'
    },
    '35830387': {
        'name': 'Sygic a.s.',
        'street': 'Twin City Tower, Mlynské nivy 16',
        'city': 'Bratislava',
        'zip_code': '82109',
        'ico': '35830387',
        'dic': '2020260714',
        'ic_dph': 'SK2020260714',
        'legal_form': 'a.s.'
    },
    '36066613': {
        'name': 'Slovensko.Digital',
        'street': 'Staré Grunty 18',
        'city': 'Bratislava',
        'zip_code': '84104',
        'ico': '36066613',
        'dic': '2020087699',
        'ic_dph': '',
        'legal_form': 'o.z.'
    },
    '44658737': {
        'name': 'Alza.sk s.r.o.',
        'street': 'Sliačska 1/D',
        'city': 'Bratislava',
        'zip_code': '83102',
        'ico': '44658737',
        'dic': '2022786894',
        'ic_dph': 'SK2022786894',
        'legal_form': 's.r.o.'
    },
    '35751291': {
        'name': 'DATART INTERNATIONAL, a.s.',
        'street': 'Plynárenská 1',
        'city': 'Bratislava',
        'zip_code': '82109',
        'ico': '35751291',
        'dic': '2020247654',
        'ic_dph': 'SK2020247654',
        'legal_form': 'a.s.'
    },
    
    # ==================== DOPRAVA ====================
    '00151742': {
        'name': 'Železnice Slovenskej republiky',
        'street': 'Klemensova 8',
        'city': 'Bratislava',
        'zip_code': '81361',
        'ico': '00151742',
        'dic': '2020480121',
        'ic_dph': '',
        'legal_form': 'štátny podnik'
    },
    '35757442': {
        'name': 'Železničná spoločnosť Slovensko, a.s.',
        'street': 'Rožňavská 1',
        'city': 'Bratislava',
        'zip_code': '83272',
        'ico': '35757442',
        'dic': '2020480200',
        'ic_dph': '',
        'legal_form': 'a.s.'
    },
    '35914921': {
        'name': 'RegioJet, a.s.',
        'street': 'U Trezorky 921/2',
        'city': 'Praha',
        'zip_code': '15800',
        'ico': '35914921',
        'dic': '4020219817',
        'ic_dph': 'SK4020219817',
        'legal_form': 'a.s.'
    },
    '00166987': {
        'name': 'Dopravný podnik Bratislava, a.s.',
        'street': 'Olejkárska 1',
        'city': 'Bratislava',
        'zip_code': '81452',
        'ico': '00166987',
        'dic': '2020430054',
        'ic_dph': 'SK2020430054',
        'legal_form': 'a.s.'
    },
    '31364501': {
        'name': 'Slovak Lines, a.s.',
        'street': 'Mlynské nivy 31',
        'city': 'Bratislava',
        'zip_code': '82109',
        'ico': '31364501',
        'dic': '2020391274',
        'ic_dph': 'SK2020391274',
        'legal_form': 'a.s.'
    },
    '36631124': {
        'name': 'FlixBus SK s.r.o.',
        'street': 'Karloveská 63',
        'city': 'Bratislava',
        'zip_code': '84104',
        'ico': '36631124',
        'dic': '2022249051',
        'ic_dph': 'SK2022249051',
        'legal_form': 's.r.o.'
    },
    
    # ==================== POISŤOVNE ====================
    '35800861': {
        'name': 'Allianz - Slovenská poisťovňa, a.s.',
        'street': 'Dostojevského rad 4',
        'city': 'Bratislava',
        'zip_code': '81574',
        'ico': '35800861',
        'dic': '2020164332',
        'ic_dph': '',
        'legal_form': 'a.s.'
    },
    '00585441': {
        'name': 'KOOPERATIVA poisťovňa, a.s.',
        'street': 'Štefanovičova 4',
        'city': 'Bratislava',
        'zip_code': '81623',
        'ico': '00585441',
        'dic': '2020409175',
        'ic_dph': '',
        'legal_form': 'a.s.'
    },
    '35812184': {
        'name': 'Generali Poisťovňa, a.s.',
        'street': 'Lamačská cesta 3/A',
        'city': 'Bratislava',
        'zip_code': '84104',
        'ico': '35812184',
        'dic': '2020260780',
        'ic_dph': '',
        'legal_form': 'a.s.'
    },
    '36857246': {
        'name': 'UNIQA poisťovňa, a.s.',
        'street': 'Krasovského 15',
        'city': 'Bratislava',
        'zip_code': '85101',
        'ico': '36857246',
        'dic': '2022589091',
        'ic_dph': '',
        'legal_form': 'a.s.'
    },
    '00603481': {
        'name': 'Slovenská kancelária poisťovateľov',
        'street': 'Trnavská cesta 82',
        'city': 'Bratislava',
        'zip_code': '82659',
        'ico': '00603481',
        'dic': '2020412892',
        'ic_dph': '',
        'legal_form': 'záujm. združ.'
    },
    '35908653': {
        'name': 'Všeobecná zdravotná poisťovňa, a.s.',
        'street': 'Panónska cesta 2',
        'city': 'Bratislava',
        'zip_code': '85104',
        'ico': '35908653',
        'dic': '2022027040',
        'ic_dph': '',
        'legal_form': 'a.s.'
    },
    '35937700': {
        'name': 'Dôvera zdravotná poisťovňa, a.s.',
        'street': 'Einsteinova 25',
        'city': 'Bratislava',
        'zip_code': '85101',
        'ico': '35937700',
        'dic': '2022119254',
        'ic_dph': '',
        'legal_form': 'a.s.'
    },
    '36284831': {
        'name': 'Union zdravotná poisťovňa, a.s.',
        'street': 'Karadžičova 10',
        'city': 'Bratislava',
        'zip_code': '81660',
        'ico': '36284831',
        'dic': '2020002085',
        'ic_dph': '',
        'legal_form': 'a.s.'
    },
    
    # ==================== STAVEBNÍCTVO ====================
    '31651518': {
        'name': 'STRABAG s.r.o.',
        'street': 'Mlynské nivy 61/A',
        'city': 'Bratislava',
        'zip_code': '82509',
        'ico': '31651518',
        'dic': '2020339661',
        'ic_dph': 'SK2020339661',
        'legal_form': 's.r.o.'
    },
    '36421928': {
        'name': 'SKANSKA SK a.s.',
        'street': 'Krajná 29',
        'city': 'Bratislava',
        'zip_code': '82104',
        'ico': '36421928',
        'dic': '2022097426',
        'ic_dph': 'SK2022097426',
        'legal_form': 'a.s.'
    },
    '00699047': {
        'name': 'PORR s.r.o.',
        'street': 'Vajnorská 167',
        'city': 'Bratislava',
        'zip_code': '83104',
        'ico': '00699047',
        'dic': '2020265936',
        'ic_dph': 'SK2020265936',
        'legal_form': 's.r.o.'
    },
    '17050189': {
        'name': 'EUROVIA SK, a.s.',
        'street': 'Osloboditeľov 66',
        'city': 'Košice',
        'zip_code': '04017',
        'ico': '17050189',
        'dic': '2020399376',
        'ic_dph': 'SK2020399376',
        'legal_form': 'a.s.'
    },
    '35830077': {
        'name': 'ZIPP BRATISLAVA spol. s r.o.',
        'street': 'Stará Vajnorská 16',
        'city': 'Bratislava',
        'zip_code': '83104',
        'ico': '35830077',
        'dic': '2020262299',
        'ic_dph': 'SK2020262299',
        'legal_form': 's.r.o.'
    },
    '31387764': {
        'name': 'YIT Slovakia a.s.',
        'street': 'Mostová 2',
        'city': 'Bratislava',
        'zip_code': '81102',
        'ico': '31387764',
        'dic': '2020387361',
        'ic_dph': 'SK2020387361',
        'legal_form': 'a.s.'
    },
    '35804262': {
        'name': 'VÁHOSTAV - SK, a.s.',
        'street': 'Priemyselná 6',
        'city': 'Žilina',
        'zip_code': '01001',
        'ico': '35804262',
        'dic': '2020100896',
        'ic_dph': 'SK2020100896',
        'legal_form': 'a.s.'
    },
    
    # ==================== AUTOMOBILOVÝ PRIEMYSEL ====================
    '35757639': {
        'name': 'Volkswagen Slovakia, a.s.',
        'street': 'J. Jonáša 1',
        'city': 'Bratislava',
        'zip_code': '84302',
        'ico': '35757639',
        'dic': '2020254047',
        'ic_dph': 'SK2020254047',
        'legal_form': 'a.s.'
    },
    '35876832': {
        'name': 'Kia Slovakia s.r.o.',
        'street': 'Sv. Jána Nepomuckého 1282/1',
        'city': 'Teplička nad Váhom',
        'zip_code': '01302',
        'ico': '35876832',
        'dic': '2021775868',
        'ic_dph': 'SK2021775868',
        'legal_form': 's.r.o.'
    },
    '35845007': {
        'name': 'Groupe PSA Slovakia s.r.o.',
        'street': 'Automobilová 1',
        'city': 'Trnava',
        'zip_code': '91701',
        'ico': '35845007',
        'dic': '2021688696',
        'ic_dph': 'SK2021688696',
        'legal_form': 's.r.o.'
    },
    '35847786': {
        'name': 'Jaguar Land Rover Slovakia s.r.o.',
        'street': 'Sládkovičova 13',
        'city': 'Nitra',
        'zip_code': '94901',
        'ico': '35847786',
        'dic': '2021693361',
        'ic_dph': 'SK2021693361',
        'legal_form': 's.r.o.'
    },
    '35874244': {
        'name': 'MATADOR Holding, a.s.',
        'street': 'Streženická cesta 45',
        'city': 'Púchov',
        'zip_code': '02001',
        'ico': '35874244',
        'dic': '2021757421',
        'ic_dph': 'SK2021757421',
        'legal_form': 'a.s.'
    },
    
    # ==================== MÉDIÁ ====================
    '35968141': {
        'name': 'Rozhlas a televízia Slovenska',
        'street': 'Mlynská dolina',
        'city': 'Bratislava',
        'zip_code': '84545',
        'ico': '35968141',
        'dic': '2021957857',
        'ic_dph': '',
        'legal_form': 'verejnoprávna inštitúcia'
    },
    '31380123': {
        'name': 'Petit Press, a.s.',
        'street': 'Lazaretská 12',
        'city': 'Bratislava',
        'zip_code': '81108',
        'ico': '31380123',
        'dic': '2020335478',
        'ic_dph': 'SK2020335478',
        'legal_form': 'a.s.'
    },
    '35700211': {
        'name': 'MARKÍZA - SLOVAKIA, spol. s r.o.',
        'street': 'Bratislavská 1/A',
        'city': 'Záhorská Bystrica',
        'zip_code': '84401',
        'ico': '35700211',
        'dic': '2020239265',
        'ic_dph': 'SK2020239265',
        'legal_form': 's.r.o.'
    },
    '31441629': {
        'name': 'MAC TV s.r.o.',
        'street': 'Brečtanová 1',
        'city': 'Bratislava',
        'zip_code': '83101',
        'ico': '31441629',
        'dic': '2020350512',
        'ic_dph': 'SK2020350512',
        'legal_form': 's.r.o.'
    },
    '35882867': {
        'name': 'News and Media Holding a.s.',
        'street': 'Einsteinova 25',
        'city': 'Bratislava',
        'zip_code': '85101',
        'ico': '35882867',
        'dic': '2021834870',
        'ic_dph': 'SK2021834870',
        'legal_form': 'a.s.'
    },
    '50497260': {
        'name': 'Aktuality.sk, a.s.',
        'street': 'Einsteinova 25',
        'city': 'Bratislava',
        'zip_code': '85101',
        'ico': '50497260',
        'dic': '2120361227',
        'ic_dph': 'SK2120361227',
        'legal_form': 'a.s.'
    },
    
    # ==================== FARMÁCIA A ZDRAVOTNÍCTVO ====================
    '31640826': {
        'name': 'PHOENIX Zdravotnícke zásobovanie, a.s.',
        'street': 'Pribylinská 2/A',
        'city': 'Bratislava',
        'zip_code': '83104',
        'ico': '31640826',
        'dic': '2020336706',
        'ic_dph': 'SK2020336706',
        'legal_form': 'a.s.'
    },
    '35810530': {
        'name': 'Dr. Max Lekáreň, a.s.',
        'street': 'Na Pántoch 18',
        'city': 'Bratislava',
        'zip_code': '83106',
        'ico': '35810530',
        'dic': '2020262132',
        'ic_dph': 'SK2020262132',
        'legal_form': 'a.s.'
    },
    '35827866': {
        'name': 'BENU Slovensko s.r.o.',
        'street': 'Karadžičova 8',
        'city': 'Bratislava',
        'zip_code': '82108',
        'ico': '35827866',
        'dic': '2020268498',
        'ic_dph': 'SK2020268498',
        'legal_form': 's.r.o.'
    },
    
    # ==================== SLUŽBY ====================
    '36017817': {
        'name': 'Slovenská pošta, a.s.',
        'street': 'Partizánska cesta 9',
        'city': 'Banská Bystrica',
        'zip_code': '97599',
        'ico': '36017817',
        'dic': '2020008776',
        'ic_dph': 'SK2020008776',
        'legal_form': 'a.s.'
    },
    '35848189': {
        'name': 'Direct Parcel Distribution SK s.r.o.',
        'street': 'Technická 7',
        'city': 'Bratislava',
        'zip_code': '82104',
        'ico': '35848189',
        'dic': '2021695989',
        'ic_dph': 'SK2021695989',
        'legal_form': 's.r.o.'
    },
    '51089301': {
        'name': 'Packeta Slovakia s.r.o.',
        'street': 'Kopčianska 92',
        'city': 'Bratislava',
        'zip_code': '85101',
        'ico': '51089301',
        'dic': '2120580493',
        'ic_dph': 'SK2120580493',
        'legal_form': 's.r.o.'
    },
    '35821256': {
        'name': 'GLS General Logistics Systems Slovakia s.r.o.',
        'street': 'Budatínska 30',
        'city': 'Bratislava',
        'zip_code': '85106',
        'ico': '35821256',
        'dic': '2020267664',
        'ic_dph': 'SK2020267664',
        'legal_form': 's.r.o.'
    },
    '35816422': {
        'name': 'TNT Express Worldwide, spol. s r.o.',
        'street': 'Ivanská cesta 22/B',
        'city': 'Bratislava',
        'zip_code': '82104',
        'ico': '35816422',
        'dic': '2020259535',
        'ic_dph': 'SK2020259535',
        'legal_form': 's.r.o.'
    },
    '46483217': {
        'name': 'Wolt Slovakia s.r.o.',
        'street': 'Digital Park II, Einsteinova 23',
        'city': 'Bratislava',
        'zip_code': '85101',
        'ico': '46483217',
        'dic': '2023416167',
        'ic_dph': 'SK2023416167',
        'legal_form': 's.r.o.'
    },
    '51069385': {
        'name': 'Bolt Operations SK s.r.o.',
        'street': 'Grösslingová 4',
        'city': 'Bratislava',
        'zip_code': '81109',
        'ico': '51069385',
        'dic': '2120564673',
        'ic_dph': 'SK2120564673',
        'legal_form': 's.r.o.'
    },
    
    # ==================== GASTRO & HoReCa ====================
    '31394965': {
        'name': 'McDonald\'s Slovakia spol. s r.o.',
        'street': 'Kamenné námestie 1',
        'city': 'Bratislava',
        'zip_code': '81499',
        'ico': '31394965',
        'dic': '2020392281',
        'ic_dph': 'SK2020392281',
        'legal_form': 's.r.o.'
    },
    '35752785': {
        'name': 'AmRest s.r.o.',
        'street': 'Galvaniho 7/D',
        'city': 'Bratislava',
        'zip_code': '82104',
        'ico': '35752785',
        'dic': '2020257126',
        'ic_dph': 'SK2020257126',
        'legal_form': 's.r.o.'
    },
    '31344593': {
        'name': 'Coca-Cola HBC Slovenská republika, s.r.o.',
        'street': 'Rajecká 28',
        'city': 'Lúka',
        'zip_code': '91623',
        'ico': '31344593',
        'dic': '2020328502',
        'ic_dph': 'SK2020328502',
        'legal_form': 's.r.o.'
    },
    '35739347': {
        'name': 'Kofola a.s.',
        'street': 'Rajecká cesta 10',
        'city': 'Rajecká Lesná',
        'zip_code': '01315',
        'ico': '35739347',
        'dic': '2020269983',
        'ic_dph': 'SK2020269983',
        'legal_form': 'a.s.'
    },
    '36238589': {
        'name': 'Heineken Slovensko, a.s.',
        'street': 'Novozámocká 2',
        'city': 'Hurbanovo',
        'zip_code': '94701',
        'ico': '36238589',
        'dic': '2020000831',
        'ic_dph': 'SK2020000831',
        'legal_form': 'a.s.'
    },
    '00599808': {
        'name': 'Pivovar Šariš, a.s.',
        'street': 'Pivovarská 9',
        'city': 'Veľký Šariš',
        'zip_code': '08221',
        'ico': '00599808',
        'dic': '2020406661',
        'ic_dph': 'SK2020406661',
        'legal_form': 'a.s.'
    },
    
    # ==================== ŠTÁTNE INŠTITÚCIE ====================
    '00151866': {
        'name': 'Sociálna poisťovňa',
        'street': '29. augusta 8 a 10',
        'city': 'Bratislava',
        'zip_code': '81363',
        'ico': '00151866',
        'dic': '2020411986',
        'ic_dph': '',
        'legal_form': 'verejnoprávna inštitúcia'
    },
    '00699063': {
        'name': 'Slovenská elektrizačná prenosová sústava, a.s.',
        'street': 'Mlynské nivy 59/A',
        'city': 'Bratislava',
        'zip_code': '82484',
        'ico': '00699063',
        'dic': '2020392696',
        'ic_dph': 'SK2020392696',
        'legal_form': 'a.s.'
    },
    '00156621': {
        'name': 'Národná diaľničná spoločnosť, a.s.',
        'street': 'Dúbravská cesta 14',
        'city': 'Bratislava',
        'zip_code': '84104',
        'ico': '00156621',
        'dic': '2020492887',
        'ic_dph': '',
        'legal_form': 'a.s.'
    },
    '17313244': {
        'name': 'Slovenská správa ciest',
        'street': 'Miletičova 19',
        'city': 'Bratislava',
        'zip_code': '82619',
        'ico': '17313244',
        'dic': '2020400116',
        'ic_dph': '',
        'legal_form': 'rozpočtová org.'
    },
    '31752942': {
        'name': 'Letisko M. R. Štefánika - Airport Bratislava, a.s.',
        'street': 'Letisko M. R. Štefánika',
        'city': 'Bratislava',
        'zip_code': '82001',
        'ico': '31752942',
        'dic': '2020334964',
        'ic_dph': 'SK2020334964',
        'legal_form': 'a.s.'
    },
    '36718556': {
        'name': 'Letisko Košice - Airport Košice, a.s.',
        'street': 'Letisko Košice 401',
        'city': 'Košice',
        'zip_code': '04175',
        'ico': '36718556',
        'dic': '2022315628',
        'ic_dph': 'SK2022315628',
        'legal_form': 'a.s.'
    },
}

def get_company(ico: str):
    """Vráti údaje firmy podľa IČO"""
    ico = ico.replace(' ', '').zfill(8)
    return SLOVAK_COMPANIES.get(ico)

def search_companies(query: str, limit: int = 10):
    """Vyhľadá firmy podľa názvu"""
    query = query.lower()
    results = []
    for ico, data in SLOVAK_COMPANIES.items():
        if query in data['name'].lower():
            results.append(data)
            if len(results) >= limit:
                break
    return results
