import psycopg
from tabulate import tabulate

valid_field_names = ["武器名", "分類", "サブ", "スペシャル"]

connection = psycopg.connect(
    host='localhost',
    dbname='game',
    user='postgres',
    password='password',
)

try:
    select_action = int(input("アクションを指定してください[0:表の表示 1:データの追加 2:データの削除]："))
    if select_action == 0:
        field_index = int(input("表示する条件を指定してください[0:条件なし 1:武器名 2:分類 3:サブ 4:スペシャル]："))
        if field_index in [1,2,3,4]:
            input_name = input("条件を入力してください：")

    elif select_action == 1:
        print("武器名, 分類, サブ, スペシャルを入力してください(改行で)")
        weapon_name = input()
        class_name = input()
        sub_name = input()
        special_name = input()

    elif select_action == 2:
        del_weapon_name = input("削除する武器名を指定してください：")

except ValueError:
    print("入力に誤りがありました")

if select_action == 0:
    if field_index == 1:
        field_name = "武器名"
    elif field_index == 2:
        field_name = "分類"
    elif field_index == 3:
        field_name = "サブ"
    elif field_index == 4:
        field_name = "スペシャル"

    if field_index == 0:
        sql1 = '''
        SELECT * FROM 武器データ;
        '''
        result = connection.execute(sql1)
    else:
        if field_name in valid_field_names:
            sql2 = f'''
            SELECT * FROM 武器データ WHERE {field_name} LIKE %s
            '''
            result = connection.execute(sql2, ("%" + input_name + "%",))
        else:
            print("無効な分類名が指定されました")

    print(tabulate(result, headers=['武器名', '分類', 'サブ', 'スペシャル'], tablefmt='simple'))

elif select_action == 1:
    try:
        sql = '''
        INSERT INTO 武器データ (武器名, 分類, サブ, スペシャル)
        VALUES (%s, %s, %s, %s);
        '''
        connection.execute(sql, [weapon_name, class_name, sub_name, special_name])
    except Exception:
        connection.rollback()
        print("データの追加が正常に完了しませんでした")
    else:
        connection.commit()
        print("データの追加が完了しました")

else:
    try:
        sql = '''
            DELETE FROM 武器データ
            WHERE 武器名 = %s;
        '''
        connection.execute(sql, [del_weapon_name])
    except Exception:
        connection.rollback()
        print("データの削除が正常に完了しませんでした")
    else:
        connection.commit()
        print("データの削除が完了しました")


