# Генератор data/parameters.csv и data/parameters.json из одного списка.
# Запуск: python -I gen_params.py
import csv, json, os

C = "code/controllers/subsystem/rogue/treasury.dm"
B = "code/__DEFINES/banking.dm"
E = "code/controllers/subsystem/rogue/economy/economy.dm"
ST = "code/modules/roguetown/roguemachine/steward/steward.dm"
NAV = "code/modules/roguetown/roguemachine/merchant/navigator.dm"
GF = "code/modules/roguetown/roguemachine/merchant/_goldface.dm"
BM = "code/modules/roguetown/roguemachine/merchant/bathmaster.dm"
LOT = "code/modules/roguetown/roguemachine/lottery.dm"
TR = "code/__DEFINES/economy/trading.dm"
PD = "code/__DEFINES/economy/pricing_defines.dm"
IQ = "code/__DEFINES/economy/internal_trade_and_quests.dm"
TG = "code/__DEFINES/economy/trade_goods.dm"
COIN = "code/game/objects/items/rogueitems/coins.dm"

P = [
 # монеты
 ("coin_gold", "Цена марки (золото)", "10", "мон.", "Номинал золотой монеты", COIN + ":224-232"),
 ("coin_silver", "Цена денария (серебро)", "5", "мон.", "Номинал серебряной монеты", COIN + ":235-242"),
 ("coin_copper", "Цена обола (медь)", "1", "мон.", "Номинал медной монеты, базовая единица", COIN + ":245-252"),
 ("coin_aalloy", "Цена псилена (древняя бронза)", "3", "мон.", "Номинал; меняла и счётный стол не принимают", COIN + ":255-262"),
 ("coin_stack", "Предел стопки монет", "20", "шт.", "Монет в одной стопке", COIN + ":6"),
 ("transfer_limit", "Предел выплаты Короны за раз", "10000", "мон.", "Максимум одной выплаты на счёт человека", C + ":358"),
 # казна
 ("treasury_seed_base", "Основа начальной казны", "1000", "мон.", "Постоянная часть начальной казны", B + ":24"),
 ("treasury_seed_rand", "Случайная часть начальной казны", "500-1500", "мон.", "rand(500, 1500) при старте", C + ":139-145"),
 ("treasury_seed_per_player", "Начальная казна на игрока", "35", "мон. на игрока", "Добавка за каждого игрока при старте", B + ":25"),
 ("rural_aid_max", "Сельская подмога, максимум", "200", "мон. в день", "Приток каждый рассвет при слабом производстве", C + ":205-229"),
 ("rural_aid_min", "Сельская подмога, минимум", "100", "мон. в день", "Когда 6 работников-производителей", "code/__DEFINES/economy/treasury.dm:5-7"),
 ("rural_aid_workers", "Работников для минимальной подмоги", "6", "чел.", "Порог производителей", "code/__DEFINES/economy/treasury.dm:5-7"),
 ("payroll_total", "Жалованье при полном составе", "460", "мон. в день", "Сумма по местам города", "modular_zz_darkages/code/modules/world/world_jobs.dm:3-14"),
 ("payroll_marshal", "Жалованье капитана стражи", "60", "мон. в день", "1 место", ST + ":76-103"),
 ("payroll_knight", "Жалованье рыцаря", "40", "мон. в день", "1 место", ST + ":76-103"),
 ("payroll_manatarms", "Жалованье латника", "30", "мон. в день", "3 места", ST + ":76-103"),
 ("payroll_warden", "Жалованье лесничего", "20", "мон. в день", "2 места", ST + ":76-103"),
 ("payroll_squire", "Жалованье рыцарского слуги", "10", "мон. в день", "1 место", ST + ":76-103"),
 ("payroll_servant", "Жалованье слуги", "20", "мон. в день", "3 места", ST + ":76-103"),
 ("payroll_physician", "Жалованье лекаря", "80", "мон. в день", "Пол по Завету; по таблице 20", "code/modules/politics/decrees/covenant_of_noc_and_pestra.dm:17-22"),
 ("payroll_apothecary", "Жалованье травника", "40", "мон. в день", "Пол по Завету; по таблице 10; 2 места", "code/modules/politics/decrees/covenant_of_noc_and_pestra.dm:17-22"),
 # ставки
 ("rate_quest", "Сбор с договоров", "20", "%", "Доля награды в казну", C + ":25-33"),
 ("rate_heads", "Сбор с голов", "15", "%", "Приёмка голов", C + ":25-33"),
 ("rate_import", "Ввозная пошлина", "15", "%", "Покупки у купца и в лавках", C + ":25-33"),
 ("rate_export", "Вывозная пошлина", "15", "%", "Мытный двор и ящик на пристани", C + ":25-33"),
 ("rate_loot", "Возвращённая добыча", "50", "%", "Захоронки разбойников", C + ":25-33"),
 ("rate_manor", "Поземельный сбор", "15", "%", "Доход поместий знати", C + ":25-33"),
 ("rate_cap", "Потолок большинства ставок", "75", "%", "Верхняя граница ставки", B + ":22"),
 ("poll_tax_max", "Подушная подать, максимум с головы", "100", "мон.", "Верхняя граница сбора", B + ":140-146"),
 ("poll_tax_count", "Число сборов подушной подати", "2", "раза за раунд", "Не раньше дня 2", B + ":141"),
 ("fine_max", "Штраф, максимум", "100", "мон.", "Также не больше 75% счёта", C + ":388-420"),
 ("fine_share", "Штраф, доля счёта", "75", "%", "Верхняя граница от счёта", C + ":388-420"),
 ("fine_bull_max", "Штраф при Золотой булле, максимум", "50", "мон.", "Также не больше 25% счёта", "code/modules/politics/decrees/golden_bull_of_kingsfield.dm"),
 ("fine_bull_share", "Штраф при Золотой булле, доля счёта", "25", "%", "", "code/modules/politics/decrees/golden_bull_of_kingsfield.dm"),
 # долги
 ("loan_min", "Личный заём, минимум", "50", "мон.", "Заём из кассы", "code/modules/roguetown/roguemachine/vaultbank.dm:535-560"),
 ("loan_max", "Личный заём, максимум", "500", "мон.", "", "code/modules/roguetown/roguemachine/vaultbank.dm:535-560"),
 ("loan_days", "Срок личного займа", "1-3", "дней", "Не позже дня 5", "code/modules/banking/loan.dm:46-55"),
 ("loan_rates", "Ставки личного займа", "10, 15, 20, 25, 50", "% в день", "На выбор", "code/modules/banking/loan.dm:46-55"),
 ("company_loan_range", "Заём казны у товарищества", "500-1500", "мон.", "Один за раз, до дня 5", B + ":56-59"),
 ("company_loan_rate", "Ставка займа у товарищества", "25", "%", "Твёрдая", B + ":56-59"),
 ("burgher_loan_min", "Беспроцентная ссуда горожан, минимум", "1000", "мон.", "Или вся нехватка, если больше", "code/modules/banking/bankruptcy.dm"),
 ("bankruptcy_floor", "Казна при описи", "2500", "мон.", "Казна ставится на это значение", B + ":39"),
 ("bankruptcy_debt", "Добавка к долгу при описи", "5000", "мон.", "", B + ":40"),
 ("bankruptcy_autoexport", "Порог излишков при описи", "25", "%", "Торговля идёт на автомат", B + ":41"),
 ("bankruptcy_recovery", "Казна при выходе из описи", "1500", "мон.", "Не ниже", B + ":44"),
 # разбой, автоввоз
 ("banditry_dangerous_base", "Разбой, опасная земля, основа", "40", "мон. в день", "Плюс 1 на игрока", "code/controllers/subsystem/rogue/economy/banditry_drain.dm:67"),
 ("banditry_dangerous_per_player", "Разбой, опасная земля, на игрока", "1", "мон. в день на игрока", "", "code/controllers/subsystem/rogue/economy/banditry_drain.dm:67"),
 ("banditry_barren_base", "Разбой, бесплодная земля, основа", "80", "мон. в день", "Плюс 2 на игрока", "code/controllers/subsystem/rogue/economy/banditry_drain.dm:67"),
 ("banditry_barren_per_player", "Разбой, бесплодная земля, на игрока", "2", "мон. в день на игрока", "", "code/controllers/subsystem/rogue/economy/banditry_drain.dm:67"),
 ("banditry_floor", "Казна не ниже при разбое", "1500", "мон.", "Остаток идёт в долг", IQ),
 ("banditry_repay", "Доля поступлений на разбойный долг", "75", "%", "", IQ),
 ("autoimport_items", "Автоввоз, число товаров", "7", "шт.", "Уголь, дерево, зерно, железная руда, шкуры, мех, жир", "code/__DEFINES/auto_import.dm:1-15"),
 ("autoimport_qty", "Автоввоз, штук за раз", "5", "шт.", "Если на складе меньше 10", "code/__DEFINES/auto_import.dm:1-15"),
 ("autoimport_min_stock", "Автоввоз, порог запаса", "10", "шт.", "Ввоз, если меньше", "code/__DEFINES/auto_import.dm:1-15"),
 ("autoimport_price_cap", "Автоввоз, потолок цены", "2", "x основы", "", "code/__DEFINES/auto_import.dm:1-15"),
 ("autoimport_floor", "Автоввоз, пол казны", "1000", "мон.", "Не ввозит ниже", "code/controllers/subsystem/rogue/economy/auto_import.dm"),
 ("autoimport_per_day", "Автоввоз, расход (оценка)", "195", "мон. в день", "До этой суммы за день, 2 дня (оценка)", "code/controllers/subsystem/rogue/economy/auto_import.dm"),
 # склад
 ("stock_buy_factor", "Склад: покупка у людей, множитель", "0,75 x 0,75", "x цены продажи", "Меньшее из 0,75 x(0,75 x S) и 0,75 x S - 1", "code/__DEFINES/economy/internal_trade_and_quests.dm"),
 ("stock_cap_days", "Предел склада, дней спроса", "2", "дня", "Диапазон 5-40 единиц", C + ":166-183"),
 ("royal_duty_base", "Порог королевской пошлины, основа", "2500", "мон. оборота", "", B + ":27"),
 ("royal_duty_per_player", "Порог королевской пошлины, на игрока", "50", "мон. оборота на игрока", "", B + ":28"),
 ("royal_duty_margin", "Королевская пошлина, наценка", "50", "%", "На прямой ввоз под заказ", B + ":29"),
 ("land_demand_growth", "Рост спроса земли на игрока", "2,5", "%", "До x3", E + ":182-221"),
 ("land_demand_cap", "Предел роста спроса земель", "3", "x", "", E + ":182-221"),
 ("land_export_factor", "Вывоз: множитель", "0,75", "x основы", "Делится на 1 + перебор", E + ":468-481"),
 ("land_batch", "Предел за один щелчок", "50", "шт.", "", E),
 ("blockade_import_mult", "Заслон: ввоз", "2", "x", "", E + ":458-466"),
 ("blockade_export_mult", "Заслон: вывоз", "0,5", "x", "", E + ":468-481"),
 ("blockade_scroll", "Свиток заслона, поручительство", "500", "ед.", "", IQ),
 ("blockade_pay", "Свиток заслона, плата", "715", "мон.", "Плюс подорожное 75 или 150", IQ),
 ("event_start", "Хозяйственные события при старте", "3", "шт.", "Держится около 5", IQ),
 ("event_days", "Длительность события", "2", "дня", "", IQ),
 ("event_shortage", "Нехватка, множитель цены", "2-3", "x", "", IQ),
 ("event_surplus", "Избыток, множитель цены", "0,5-0,7", "x", "", IQ),
 # заказы
 ("order_base_mult", "Постоянный заказ, множитель основы", "2,5", "x", "За единицу товара", E + ":483-526"),
 ("order_partial", "Частичная сдача", "85", "%", "", E + ":581-694"),
 ("order_petition", "Плата по прошению", "80", "%", "", "code/modules/roguetown/roguestock/steward_petition.dm:138"),
 ("order_new_per_day", "Новых заказов в день, основа", "4", "шт.", "Плюс 1 на 20 игроков", E + ":240-283"),
 ("order_pool_max", "Заказов в пуле, максимум", "13", "шт.", "До 3 на землю", E + ":240-283"),
 ("order_days", "Срок заказа", "2", "дня", "Срочные на 1 день, до 2", E + ":240-283"),
 ("petition_max", "Прошений в день", "3", "шт.", "Поручительство 200-400", "code/modules/roguetown/roguestock/steward_petition.dm"),
 # поручительство
 ("pledge_start", "Поручительство, старт", "1000", "ед.", "", B + ":4-11"),
 ("pledge_refill_base", "Поручительство, пополнение в день", "500", "ед.", "Плюс 4 на игрока, пока стоит Золотая булла", B + ":4-11"),
 ("pledge_refill_per_player", "Поручительство, на игрока", "4", "ед. на игрока", "", B + ":4-11"),
 ("assembly_trade_cap", "Потолок торговли ратмана", "0-900", "мон. в день", "", "code/controllers/subsystem/rogue/city_assembly"),
 ("assembly_defence_cap", "Потолок обороны ратмана", "0-1000", "ед.", "Поручительство", "code/controllers/subsystem/rogue/city_assembly"),
 # кассы
 ("church_seed", "Церковная касса, старт", "1000", "мон.", "", B + ":117-126"),
 ("merchant_seed", "Касса купца, старт", "500", "мон.", "", B + ":124"),
 ("bathhouse_seed", "Касса бани, старт", "500", "мон.", "", B + ":125"),
 ("bath_staff_pay", "Работникам бани из кассы", "50", "мон. в день", "", B + ":152-154"),
 ("inn_cut", "Доля трактира с договоров", "5", "%", "", "code/modules/roguetown/roguemachine/questing/contract_ledger/innkeeper.dm:112-126"),
 # доходы людей
 ("estate_ispan", "Доход с поместий: ишпан", "275", "мон. в день", "", "code/modules/jobs/job_types/roguetown/nobility/lord.dm:255"),
 ("estate_merchant", "Доход с поместий: купец", "100", "мон. в день", "", "code/modules/jobs/job_types/roguetown/burghers/merchant.dm:16"),
 ("estate_consort", "Доход с поместий: супруг ишпана", "22", "мон. в день", "", B + ":31"),
 ("estate_marshal", "Доход с поместий: капитан стражи", "20", "мон. в день", "", B + ":31"),
 ("estate_steward", "Доход с поместий: казначей", "16", "мон. в день", "", B + ":31"),
 ("estate_knight", "Доход с поместий: рыцарь", "15", "мон. в день", "", B + ":31"),
 ("estate_total", "Доход с поместий, всего (оценка)", "450", "мон. в день", "Оценка по составу", C + ":452-480"),
 ("ispan_start", "Твёрдый начальный вклад ишпана", "250", "мон.", "", "code/modules/jobs/job_types/roguetown/nobility/lord.dm"),
 ("people_start_per_player", "Начальные счета и кошели (оценка)", "120", "мон. на игрока", "Оценка: около 3000 при 25 игроках", "code/__DEFINES/jobs.dm:302-309"),
 ("guild_total", "Договоры цеха (оценка)", "400", "мон. в день", "Оценка: около 2400 за раунд", "code/modules/roguetown/roguemachine/questing/types/__quest.dm:295-336"),
 ("quest_light", "Договор лёгкий", "40", "мон.", "Около", "code/modules/roguetown/roguemachine/questing/types/__quest.dm:295-336"),
 ("quest_clear", "Договор зачистки", "85", "мон.", "Около", "code/modules/roguetown/roguemachine/questing/types/__quest.dm:295-336"),
 ("quest_raid", "Договор налёта", "155", "мон.", "Около", "code/modules/roguetown/roguemachine/questing/types/__quest.dm:295-336"),
 ("quest_invasion", "Договор вторжения", "350", "мон.", "Около", "code/modules/roguetown/roguemachine/questing/types/__quest.dm:295-336"),
 ("head_bounty_min", "Награда за голову, от", "125", "мон.", "", "code/modules/roguetown/roguemachine/questing/types/kill/__quest_kill_base.dm:360-369"),
 # мытный двор
 ("nav_fee", "Сбор купца с мытного двора", "15", "%", "Может быть до 50%", NAV + ":372-450"),
 ("nav_duty", "Пошлина мытного двора", "15", "%", "", NAV + ":411-436"),
 ("nav_take_home", "Выплата игроку (приблизительно)", "70", "%", "От цены с насыщением и спросом", NAV + ":372-450"),
 ("nav_demand", "Спрос мытного двора", "0,5-1,5", "x", "", NAV),
 ("nav_noship", "Разряд без корабля", "0,5", "x", "Кроме ценностей, рыбы, гончарного, резного", PD),
 ("nav_ship_max", "Разряд с кораблём, максимум", "1,5", "x", "", PD),
 ("nav_start_range", "Склады разрядов при старте", "0,7-1,3", "x", "", PD),
 ("nav_per_player", "Склады разрядов, на игрока сверх 15", "0,5", "%", "", PD),
 ("nav_smuggler", "Посредник тайной перевалки", "50", "%", "С работником бани 0%", TR),
 ("crate_cut", "Доля купца с ящика на пристани", "25", "%", "", "code/modules/roguetown/roguemachine/merchant/trade/fulfillment_crate.dm:396-425"),
 ("goldface_fee", "Пошлина лавки купца", "15", "%", "", GF + ":199-206"),
 ("goldface_public_fee", "Надбавка товарной лавки", "50", "%", "", TR),
 # корабли
 ("ship_rolls", "Бросков кораблей в день", "8", "шт.", "", TR),
 ("ship_dock", "Мест у причала", "2", "шт.", "До 4", TR),
 ("ship_stay", "Стоянка корабля", "60", "мин", "Отослать можно через 20", TR),
 ("ship_buy_markup", "Корабль покупает оптом, наценка", "3,5", "x", "Для основных товаров, максимум", TR),
 ("ship_sell_discount", "Корабль продаёт, скидка", "50", "%", "", TR),
 ("upgrade_dock", "Улучшение: причал", "1250", "расположения", "", TR),
 ("upgrade_gnome", "Улучшение: гномья артель", "2500", "расположения", "", TR),
 ("upgrade_hail", "Улучшение: окликатель", "500", "расположения", "", TR),
 ("upgrade_arsenal", "Улучшение: арсенал", "750", "расположения", "", TR),
 ("upgrade_caravan", "Улучшение: подземный караван", "500", "расположения", "", TR),
 ("upgrade_call", "Улучшение: вызов корабля", "250", "расположения", "", TR),
 ("kinship_buy", "Землячество, скидка на покупки", "10", "%", "", "code/controllers/subsystem/rogue/merchant_trade_kinship.dm"),
 ("kinship_sell", "Землячество, надбавка на продажи", "10", "%", "", "code/controllers/subsystem/rogue/merchant_trade_kinship.dm"),
 # баня
 ("bath_rate", "Банный клад, доля стоимости", "15", "%", "За каждый заход", BM + ":428-497"),
 ("bath_period", "Банный клад, период", "6", "мин", "", BM + ":428-497"),
 ("bath_radius", "Банный клад, радиус от кассы", "5", "клеток", "", BM + ":428-497"),
 ("bath_repeat", "Банный клад, множитель за копию", "0,7", "x", "Для повтора того же типа", BM + ":428-497"),
 ("bath_church", "Банный клад, десятина Церкви", "20", "%", "", B + ":117-126"),
 # прочее
 ("wheel_stake_min", "Колесо Фортуны, ставка от", "5", "мон.", "", LOT + ":15-22"),
 ("wheel_stake_max", "Колесо Фортуны, ставка до", "100", "мон.", "", LOT + ":15-22"),
 ("wheel_win_chance", "Колесо Фортуны, шанс выигрыша", "60", "% + (Удача - 2)", "", LOT + ":70-110"),
 ("wheel_mult_avg", "Колесо Фортуны, средний выигрыш", "1,28", "x ставки", "Диапазон 1,1-2", LOT + ":70-110"),
 ("escrow_markup", "Стол заказов: надбавка", "70", "%", "Цена = материал + 70% + 5", "code/modules/roguetown/roguemachine/escrow.dm"),
 ("escrow_flat", "Стол заказов: фикс", "5", "мон.", "", "code/modules/roguetown/roguemachine/escrow.dm"),
 ("scrapper_seed", "Приёмник лома, бюджет", "50", "мон.", "Начало", TR),
 ("mail_fee", "Почта, плата за письмо", "1", "мон.", "", "code/modules/roguetown/roguemachine/mail.dm:598"),
 ("round_minutes", "Длительность раунда", "165", "мин", "", "code/_compile_options.dm:11"),
 ("day_minutes", "Игровые сутки", "29", "мин", "Около, множитель времени 50", "code/controllers/subsystem/ticker.dm:42"),
 ("markup_weapon", "Наценка: доспех и оружие", "1,5", "x", "", PD),
 ("markup_light_armor", "Наценка: лёгкий доспех", "2", "x", "", PD),
 ("markup_plain_clothes", "Наценка: простая одежда", "2,5", "x", "", PD),
 ("markup_fine_clothes", "Наценка: нарядная одежда", "3,5", "x", "", PD),
 ("markup_carved", "Наценка: резное", "2", "x", "", PD),
 ("markup_trophy", "Наценка: трофеи", "2", "x", "", PD),
 ("markup_potion", "Наценка: снадобья", "1,8", "x", "", PD),
 ("markup_food", "Наценка: свежая еда", "1,5", "x", "", PD),
 ("markup_stores", "Наценка: запасы", "1,7", "x", "", PD),
 ("markup_books", "Наценка: книги и инструменты музыки", "1,7", "x", "", PD),
 ("markup_raw", "Наценка: сырьё", "1", "x", "", PD),
]

here = os.path.dirname(os.path.abspath(__file__))
data = os.path.normpath(os.path.join(here, "..", "data"))
os.makedirs(data, exist_ok=True)
ids = [p[0] for p in P]
assert len(ids) == len(set(ids)), "повтор id"
rows = [dict(id=a, name=b, value=c, unit=d, meaning=e, code=f) for a, b, c, d, e, f in P]
with open(os.path.join(data, "parameters.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump({"version": "2026-11-15", "count": len(rows), "parameters": rows}, f, ensure_ascii=False, indent=1)
with open(os.path.join(data, "parameters.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";", lineterminator="\r\n")
    w.writerow(["id", "Параметр", "Значение", "Единица", "Что означает", "Адрес в коде"])
    for r in rows:
        w.writerow([r["id"], r["name"], r["value"], r["unit"], r["meaning"], r["code"]])
print("параметров:", len(rows))
