from random import sample

version = '0.1'
starting_cash = 5000
bet_amount = 500
possible_cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

class Hand:
    cards = []

    def __init__(self, deal_initial=False):
        if deal_initial and len(self.cards) == 0:
            self.deal_cards()

    def cleanup_scores(self, scores):
        new_scores = [numba for numba in filter(lambda x : x <= 21, scores)]
        if len(new_scores) == 0:
            new_scores = [min(scores)]
        return new_scores

    def get_score(self):
        scores = [0]
        for card in self.cards:
            if card == 'A':
                scores1  = [score + 1 for score in scores]
                scores10 = [score + 10 for score in scores]
                scores11 = [score + 11 for score in scores]
                scores = self.cleanup_scores(scores1 + scores10 + scores11)
            elif card == 'J' or card == 'Q' or card == 'K':
                scores = [score + 10 for score in scores]
                scores = self.cleanup_scores(scores)
            else:
                scores = [score + int(card) for score in scores]
                scores = self.cleanup_scores(scores)
        
        return max(scores)
    
    def hit(self):
        sampled_card = (sample(possible_cards, 1))
        self.cards = self.cards + sampled_card
        return sampled_card[0]

    def renew_hand(self):
        self.cards = []
    
    def deal_cards(self):
        self.hit()
        self.hit()
    
    def get_num_of_cards(self):
        return len(self.cards)

    def get_hand(self):
        return self.cards

    def print_hand(self):
        return "[ {0} ]".format(','.join(self.cards))

class Player:
    cash   = starting_cash
    bet    = bet_amount
    hand   = None
    silent = False
    name = ""

    def __init__(self, silent=False, name="Justin"):
        self.silent = silent
        self.hand = Hand()
        self.name = name

    def deal(self):
        self.hand.renew_hand()
        self.hand.deal_cards()
        if not self.silent:
            print("You've been dealt a {0} hand, with a score of {1}. Good luck!".format(self.hand.print_hand(), self.hand.get_score()))
    
    def check_score(self):
        if self.hand.get_num_of_cards() == 5:
            if not self.silent:
                print("You've already drawn 5 cards, you can't hit for more cards! Oops!")
            return False
        if self.hand.get_score() > 21:
            if not self.silent:
                print("You've bust, you can't hit for more cards! Oops!")
            return False
        if not self.silent:
            print("You currently hold {0}, with a best score of {1}.".format(self.hand.print_hand(), self.hand.get_score()))
        return True
    
    def get_name(self):
        return self.name

    def get_bet(self):
        return self.bet
    
    def get_score(self):
        return self.hand.get_score()

    def hit(self):
        return self.hand.hit()

    def pay(self, other, amount):
        self.cash = self.cash - amount
        other.cash = other.cash + amount

    def get_balance(self):
        return self.cash

    def print_hand(self):
        return self.hand.print_hand()

    def get_hand(self):
        return self.hand.get_hand()
    
def get_confirmation(message):
    result = False
    while True:
        resp = input(message).lower()
        if resp == 'yes' or resp == 'y':
            result = True
            break
        elif resp == 'no' or resp == 'n':
            break
        print('Sorry, expected yes or no (y/n) response.')
    return result

def check_payout(player):
    mult = 1
    hand = player.get_hand()

    if len(hand) == 5:
        mult = mult * 5

    if player.get_score() == 21:
        mult = mult * 2
    return mult

def main():
    print("Welcome to Justin's PyBlackJack v{0}! ".format(version))
    print("Enjoy some good ol' one on one. You start with a balance of ${0}, good luck!".format(starting_cash))
    # Assume 1 player for now (with AI dealer)
    me = Player(name=input("Please enter your name: "))
    ai = Player(silent=True)

    # Start new round
    while True:
        print('---starting round---')

        ai.deal()
        me.deal()

        while True:
            if me.check_score() and get_confirmation("Do you want to hit (y/n): "):
                print("You hit, and got a {0}!".format(me.hit()))
            else:
                break

        while True:
            if ai.check_score() and ai.get_score() < 18:
                ai.hit()
            else:
                break

        print()
        print("The dealer reveals his hand! He got {0}, with a score of {1}!".format(ai.print_hand(), ai.get_score()))
        
        if ai.get_score() > 21:
            win_amount = me.get_bet() * check_payout(me)
            print('Player {0} wins ${1} from the dealer!'.format(me.get_name(), win_amount))
            ai.pay(me, win_amount)

        elif ai.get_score() == me.get_score():
            print('Both player {0} and dealer got the same score, draw!'.format(me.get_name()))

        elif me.get_score() > ai.get_score() and me.get_score() < 22:
            win_amount = me.get_bet() * check_payout(me)
            print('Player {0} wins ${1} from the dealer!'.format(me.get_name(), win_amount))
            ai.pay(me, win_amount)
        
        else:
            win_amount = me.get_bet() * check_payout(ai)
            print('Dealer wins ${0} from the Player {1}!'.format(win_amount, me.get_name()))
            me.pay(ai, win_amount)
        
        print('[Current balances]')
        print('ai:', ai.get_balance())
        print('me:', me.get_balance())
        print()
        if not get_confirmation("Do you want to play a new round (y/n): "):
            if ai.get_balance() > me.get_balance():
                print('You lose, better luck next time!')
            else:
                print('You win, congratulations!')
            print('Thanks for playing PyBlackJack v{0}! Come back soon!'.format(version))
            break
        else:
            print('Beginning new round! May the luck be with you!')

main()
