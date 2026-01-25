import random
import time

class Connect:
    def __init__(self, nb_def):
        self.nb_def = nb_def
        self.coeff_lose = 1 * (3/4)**nb_def
        self.grid = [['_', '_', '_', '_', '_', '_', '_'],
                     ['_', '_', '_', '_', '_', '_', '_'],
                     ['_', '_', '_', '_', '_', '_', '_'],
                     ['_', '_', '_', '_', '_', '_', '_'],
                     ['_', '_', '_', '_', '_', '_', '_'],
                     ['_', '_', '_', '_', '_', '_', '_']]
        self.tours = 0
        self.is_full = [False, False, False, False, False, False, False]
        
        self.last_played = '_'
        self.last_played_col = random.randint(0, 6)
        
        
# /------------------------ FONCTIONS AUXILIAIRES ------------------------\

    # Trouver l'index du fond
    def hit_bottom(self, col):
        i = 0
        while i < 6 and self.grid[i][col] == '_':
            i += 1
        return i
    
    
    # Vérifie les nb-series de d'un caractère dans une orientation donnée
    def verif(self, lign, col, char, orien):
        if self.grid[lign][col] != char or char == '_':
            return 0
        
        if (orien[:3] == "hau" and lign == 0) or (orien[:3] == "bas" and lign == 5) or (orien[-3:] == "gau" and col == 0) or (orien[-3:] == "dra" and col == 6): # Pour les bords
            return 1
        
        ln = len(orien)
        nlg, ncl = lign, col
        if ln != 3 and ln != 7:
            raise ValueError("Incorrect len of orien")
        
        # Vérifie déjà pour haut et bas (s'ils existent)
        if orien[:3] == "hau":
            nlg -= 1
        elif orien[:3] == "bas":
            nlg += 1
        
        # Vérifie les cotés (et diagonales)
        if orien[-3:] == "gau":
            ncl -= 1
        elif orien[-3:] == "dra":
            ncl += 1
        
        # Vérif si certaines valeurs ont changés, puis retourne
        if nlg == lign and ncl == col:
            raise ValueError("Incorrect arg in orien")
        return 1 + self.verif(nlg, ncl, char, orien)
            
        
    # Verifie qui a gagné
    def who_has_win(self):
        char = self.last_played
        if char == 'O':
            print("Player won")
        elif char == 'X':
            print("Bot won")
        else:
            raise ValueError("Not valid token")
    
    
        
    # Génère les cases valides
    def generate(self, lign, cln):
        lst = []
        if cln > 0:
            if self.grid[lign][cln-1] != '_':
                lst.append([0, -1, "gau"])
            if lign > 0 and self.grid[lign-1][cln-1] != '_':
                lst.append([-1, -1, "hau-gau"])
            if lign < 5 and self.grid[lign+1][cln-1] != '_':
                lst.append([1, -1, "bas-gau"])
        if cln < 6:
            if self.grid[lign][cln+1] != '_':
                lst.append([0, 1, "dra"])
            if lign > 0 and self.grid[lign-1][cln+1] != '_':
                lst.append([-1, 1, "hau-dra"])
            if lign < 5 and self.grid[lign+1][cln+1] != '_':
                lst.append([1, 1, "bas-dra"])
        if lign < 5 and self.grid[lign+1][cln] != '_':
            lst.append([1, 0, "bas"])
        return lst
            
    
# \-----------------------------------------------------------------------/
    
    
    # Au tour du joueur
    def play_move(self, col):
        i = self.hit_bottom(col) - 1
        if self.is_full[col] == False:
            self.last_played = 'O'
            self.last_played_col = col
            self.grid[i][col] = 'O'
            self.tours += 1
            #self.show()
            if self.has_win():
                print("Congratulations")
            else:
                if i == 0:
                    self.is_full[col] = True
                time.sleep(3)
                self.bot_move()
        else:
            print("Full")
    
    
    # Vérifie si le joueur ou le bot à gagné
    def has_win(self):
        if self.tours < 4:
            #print("has_win: Too Early")
            return False
        lign = self.hit_bottom(self.last_played_col)
        col = self.last_played_col
        char = self.last_played
        dg_hau = self.verif(lign, col, char, "bas-gau") + self.verif(lign, col, char, "hau-dra") - 1
        horiz = self.verif(lign, col, char, "gau") + self.verif(lign, col, char, "dra") - 1
        dg_bas = self.verif(lign, col, char, "hau-gau") + self.verif(lign, col, char, "bas-dra") - 1
        vertic = self.verif(lign, col, char, "bas")
        if dg_hau >= 4 or horiz >= 4 or dg_bas >= 4 or vertic >= 4:
            self.who_has_win()
            return True
        return False
             
        
    # Au tour du bot
    def bot_move(self):
        coeff_rand = random.random()
        #print("coeff_rand :", coeff_rand, "coeff_lose :", self.coeff_lose)
        col = -1
        # Est-ce qu'il décide d'être intelligent ?
        if coeff_rand < self.coeff_lose:
            #print("Intelligent way")
            
            # Quoi faire pour les 4 premiers tours
            if self.tours < 4:
                binf, bsup = self.last_played_col, self.last_played_col
                if self.last_played_col > 0:
                    binf -= 1
                if self.last_played_col < 6:
                    bsup += 1
                #print(binf, bsup)
                col = random.randint(binf, bsup)
                
            # Quoi faire le reste du temps
            else:
                id_imp = -1
                list_prim = []
                for cln in range(7):
                    #print("colonne: ", cln)
                    if self.is_full[cln] == False:
                        lign = self.hit_bottom(cln) - 1
                        lc = self.generate(lign, cln)
                        #print(lc)
                        ln_cps = len(lc)
                        for i in range(ln_cps):
                            nb_ser = self.verif(lign+lc[i][0], cln+lc[i][1], self.grid[lign+lc[i][0]][cln+lc[i][1]], lc[i][2])
                            #print("nb_ser: ", nb_ser)
                            if nb_ser >= 3:
                                id_imp = cln
                                #print("id_imp: ", id_imp)
                                break
                            elif nb_ser == 2:
                                list_prim.append(cln)
                                print("list_prim: ", list_prim)
                    if id_imp >= 0:
                        break
                if id_imp >= 0:
                    col = id_imp
                elif len(list_prim) != 0:
                    col = random.choice(list_prim)
                else:
                    while True:
                        col = random.randint(0, 6)
                        if self.is_full[col] == False:
                            break
                
        # Là, non.
        else:
            #print("Dumb way")
            
            while True:
                col = random.randint(0, 6)
                if self.is_full[col] == False:
                    break
        
        # Action de fin
        #print(col)
        self.last_played = 'X'
        self.last_played_col = col
        i = self.hit_bottom(col)-1
        self.grid[i][col] = 'X'
        self.tours += 1
        #self.show()
        if self.has_win():
            print("Try Again")
        else:
            if i == 0:
                self.is_full[col] = True
    
    
    # Afficher la grille
    def show(self):
        for i in range(6):
            print(self.grid[i])
        print("  0    1    2    3    4    5    6")
        
    # Retourner la grille
    def ret_grid(self):
        return self.grid

    
Test = Connect(0)

Test.show()

