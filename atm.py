import json
url = 'card_pass.json' #카드의 번화와 비번이 있는 파일
with open(url, 'r') as f:
    data = json.load(f)
url2 = 'bank balance.json'#계좌당 잔고
with open(url2, 'r') as f:
    balance = json.load(f)
url3= 'atm.json'# atm 잔고
with open(url3, 'r') as f:
    atm_balance = json.load(f)
 
class ATM():
    def __init__(self):
        self.card_num = None 
        self.password_num = None
        self.balance_money = None
        self.account_num = None


    def card(self,x): #card 삽입
        if x in data['credit'].keys():
            self.card_num = x
            return True
        else:
            print('This card is Wrong card')
            print('Insert the card again')
            return False

    def password(self, x):#비밀번호 입력
        if int(x) == data['credit'][self.card_num]:
            return True
        else:
            print('you enter Wrong PIN number')
            return False
    

    def account(self):#계좌번호 확인
        self.account_num = data['account'][self.card_num]
        print('account number:', data['account'][self.card_num])
        self.balance_money = balance[self.account_num]

    def check_balance(self): # 현재 계좌 잔액 확인

        print('The balance in your current account is:', self.balance_money)

    def Deposit(self): # 계좌에 입금
        print('Please select the amount to deposit:')
        dollar_100=int(input('100 dollar:',))
        dollar_50=int(input('50 dollar:',))
        dollar_20=int(input('20 dollar:',))
        dollar_10=int(input('10 dollar:',))
        dollar_5=int(input('5 dollar:',))
        dollar_2=int(input('2 dollar:',))
        dollar_1=int(input('1 dollar:',))
        money = dollar_100*100+dollar_50*50+dollar_20*20+dollar_10*10+dollar_5*5+dollar_2*2+dollar_1
        
        print(f'Is the deposit amount  {money} dollar.?')
        print("If it is right insert y or n if not correct")
        y = input()
        if y == 'y':
            self.balance_money = self.balance_money + money
            print(f'The balance in your current account is: {self.balance_money} dolloar')
            balance[self.account_num] = self.balance_money
            atm_balance['100'] += dollar_100
            atm_balance['50'] += dollar_50
            atm_balance['20'] += dollar_20
            atm_balance['10'] += dollar_10
            atm_balance['5'] += dollar_5
            atm_balance['2'] += dollar_2
            atm_balance['1'] += dollar_1
        
            with open(url2, "w") as f: 
                json.dump(balance, f,indent=1)
            with open(url3, "w") as f: 
                json.dump(atm_balance, f,indent=1)
        
        
    
    def withdrawal(self): #계좌에서 출금
        money = int(input('Enter the amount of money to be withdrawn:'))
        print(f'Is the withdrawn amount {money} dollar.?')
        print("If it is right insert y or n if not correct") 
        y = input()
        if money > self.balance_money:
            return print('Your balance is low.')
        elif y == 'y':
            dollor = self.cal(money)
            if not dollor:
                return print('Atm machine has insufficient balance.')
            print(dollor)
            self.balance_money = self.balance_money - money
            print(f'The balance in your current account is: {self.balance_money} dolloar')
            balance[self.account_num] = self.balance_money
            with open(url2, "w") as f: 
                json.dump(balance, f,indent=1)
            with open(url3, "w") as f: 
                json.dump(atm_balance, f,indent=1)
    


    def send(self): #송금
        account2= input('Write down the account number you want to transfer: ')
        if account2 in balance.keys():
            money = int(input('Enter the amount to remit:'))
            print(f'Is the remit amount {money} dollar?')
            print("If it is right insert y or n if not correct")
            y = input()
            if y == 'y':
                self.balance_money = self.balance_money - money
                balance[account2] += money
                print(f'The balance in your current account is: {self.balance_money} dolloar')
                balance[self.account_num] = self.balance_money
                
                with open(url2, "w") as f: 
                    json.dump(balance, f,indent=1)
        else:
            print('you wrote down the wrong account number.')
    
    def cal(self, x): #몇장의 지폐를 주어야 할지 계산하는 함수
        money = int(x)
        money, dollar_100 = self.paper_num(money, 100)
        atm_balance['100'] -=dollar_100
        money, dollar_50 = self.paper_num(money, 50)
        atm_balance['50'] -=dollar_50
        money, dollar_20 = self.paper_num(money, 20)
        atm_balance['20'] -=dollar_20
        money, dollar_10 = self.paper_num(money, 10)
        atm_balance['10'] -=dollar_10
        money, dollar_5 = self.paper_num(money, 5)
        atm_balance['5'] -=dollar_5
        money, dollar_2 = self.paper_num(money, 2)
        atm_balance['2'] -=dollar_2
        money, dollar_1 = self.paper_num(money, 1)
        atm_balance['1'] -=dollar_1
        if money == 0:
            return {100:dollar_100, 50: dollar_50, 20:dollar_20,10: dollar_10, 5:dollar_5, 2:dollar_2, 1:dollar_1}
        else:
            return False

    def paper_num(self, money, amount):
        num = money//amount
        if amount == 100:
            rest = atm_balance['100']
        elif amount == 50:
            rest = atm_balance['50']
        elif amount == 20:
            rest = atm_balance['20']
        elif amount == 10:
            rest = atm_balance['10']
        elif amount == 5:
            rest = atm_balance['5']
        elif amount == 2:
            rest = atm_balance['2']
        elif amount == 1:
            rest = atm_balance['1']
        if rest >= num:
            money = money-amount*num
        else:
            num = rest
            money = money -amount*num
        rest = rest-num
        return money, num

def atm_api():
    atm= ATM()
    while True:
        print('please insert your credit card')
        a= atm.card(input())
        if not a:
            print()
            continue
        print('Please enter your Pin Number')
        a= atm.password(input())
        if not a:
            print()
            continue
        atm.account()
        while True:
            print("Select the task you want.")
            print("If you want to check the balance, type 1. If you want to deposit money, type 2. If you want to withdraw money, type 3. If you want to transfer money, type 4. If you want to finish, type 5")
            x= input()
            if x == '1':
                atm.check_balance()
            elif x=='2':
                atm.Deposit()
            elif x=='3':
                atm.withdrawal()
            elif x=='4':
                atm.send()
            else:
                print()
                break
            print()

atm_api()
