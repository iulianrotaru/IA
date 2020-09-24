import time

import pygame, sys


def deseneaza_gridCell(display, tabla, lin, col):
    w_gr = h_gr = 50

    x_img = pygame.image.load('ics.png')
    x_img = pygame.transform.scale(x_img, (w_gr, h_gr))
    zero_img = pygame.image.load('zero.png')
    zero_img = pygame.transform.scale(zero_img, (w_gr, h_gr))
    drt = []
    for ind in range(len(tabla)):
        linie = ind // 10
        coloana = ind % 10
        patr = pygame.Rect(coloana * (w_gr + 1), linie * (h_gr + 1), w_gr, h_gr)
        print(str(coloana * (w_gr + 1)), str(linie * (h_gr + 1)))
        drt.append(patr)
        if lin == linie and col == coloana:
            pygame.draw.rect(display, (0, 0, 255), patr)
        elif tabla[ind] == 'x':
            pygame.draw.rect(display, (254, 195, 172), patr)
        elif tabla[ind] == '0':
            pygame.draw.rect(display, (206, 206, 206), patr)
        else:
            pygame.draw.rect(display, (255, 255, 255), patr)

        if tabla[ind] == 'x':
            display.blit(x_img, (coloana * (w_gr + 1), linie * (h_gr + 1)))
        elif tabla[ind] == '0':
            display.blit(zero_img, (coloana * (w_gr + 1), linie * (h_gr + 1)))
    pygame.display.flip()
    return drt

def deseneaza_grid(display, tabla):
    w_gr = h_gr = 50

    x_img = pygame.image.load('ics.png')
    x_img = pygame.transform.scale(x_img, (w_gr, h_gr))
    zero_img = pygame.image.load('zero.png')
    zero_img = pygame.transform.scale(zero_img, (w_gr, h_gr))
    drt = []
    for ind in range(len(tabla)):
        linie = ind // 10
        coloana = ind % 10
        patr = pygame.Rect(coloana * (w_gr + 1), linie * (h_gr + 1), w_gr, h_gr)
        print(str(coloana * (w_gr + 1)), str(linie * (h_gr + 1)))
        drt.append(patr)
        if tabla[ind] == 'x':
            pygame.draw.rect(display, (254, 195, 172), patr)
        elif tabla[ind] == '0':
            pygame.draw.rect(display, (206, 206, 206), patr)
        else:
            pygame.draw.rect(display, (255, 255, 255), patr)
        if tabla[ind] == 'x':
            display.blit(x_img, (coloana * (w_gr + 1), linie * (h_gr + 1)))
        elif tabla[ind] == '0':
            display.blit(zero_img, (coloana * (w_gr + 1), linie * (h_gr + 1)))
    pygame.display.flip()
    return drt


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 10
    JMIN = None
    JMAX = None
    GOL = '#'

    def __init__(self, tabla=None):
        if tabla == None:
            self.matr = [self.__class__.GOL] * 100
            self.matr[44] = 'x'
            self.matr[54] = 'x'
            self.matr[45] = '0'
            self.matr[55] = '0'
        else:
            self.matr = tabla

    def getScore(self,jucator):
        rez = 0
        # primul tip de diagonale i,j-> i+1,j+1 -> i+2,j+2
        for i in range(8):
            for j in range(8):
                if self.matr[i * 10 + j] == self.matr[(i + 1) * 10 + (j + 1)] and self.matr[i * 10 + j] == self.matr[
                    (i + 2) * 10 + (j + 2)]:
                    if self.matr[i * 10 + j] == jucator:
                        rez = rez + 1

        # al doilea tip de diagonale i,j-> i-1,j+1 -> i-2,j+2
        for i in range(2, 10):
            for j in range(8):
                if self.matr[i * 10 + j] == self.matr[(i - 1) * 10 + (j + 1)] and self.matr[i * 10 + j] == self.matr[
                    (i - 2) * 10 + (j + 2)]:
                    if self.matr[i * 10 + j] == jucator:
                        rez = rez + 1

        return rez

    def final(self):
        # mai intai verific daca se pot pune piese
        rez = len(self.mutari(self.__class__.JMIN))==0 or len(self.mutari(self.__class__.JMAX))==0

        if (rez):
            # aici trebuie sa stabilim cum se termina jocul
            scorX = 0
            scor0 = 0

            # primul tip de diagonale i,j-> i+1,j+1 -> i+2,j+2
            for i in range(8):
                for j in range(8):
                    if self.matr[i * 10 + j] == self.matr[(i+1) * 10 + (j+1)] and self.matr[i * 10 + j] == self.matr[(i+2) * 10 + (j+2)]:
                        if self.matr[i * 10 + j] == 'x':
                            scorX = scorX + 1
                        elif self.matr[i * 10 + j] == '0':
                            scor0 = scor0 + 1

            # al doilea tip de diagonale i,j-> i-1,j+1 -> i-2,j+2
            for i in range(2,10):
                for j in range(8):
                    if self.matr[i * 10 + j] == self.matr[(i-1) * 10 + (j+1)] and self.matr[i * 10 + j] == self.matr[(i-2) * 10 + (j+2)]:
                        if self.matr[i * 10 + j] == 'x':
                            scorX = scorX + 1
                        elif self.matr[i * 10 + j] == '0':
                            scor0 = scor0 + 1

            if scor0 == scorX:
                return 'remiza'
            elif scor0 > scorX:
                return '0'
            else:
                return 'x'

        else: # daca unul dintre jucatori mai are piese return false
            return False

    def vecini(self,xx,xy,yx,yy):
        dx = [-1, -1, -1, 0, 0, 1, 1, 1]
        dy = [-1, 0, 1, 1, -1, -1, 0, 1]
        gasitX = 0
        gasit0 = 0
        for i in range(8):
            lin = dx[i] + xx
            col = dy[i] + xy

            # verific sa nu ies din matrice
            if lin >= 0 and lin < 10 and col >= 0 and col < 10:

                # verific daca gasesc vreun x
                if self.matr[lin * 10 + col] == 'x':
                    gasitX = 1
                # verific daca gasesc vreun 0
                elif self.matr[lin * 10 + col] == '0':
                    gasit0 = 1

            lin = dx[i] + yx
            col = dy[i] + yy

            # verific sa nu ies din matrice
            if lin >= 0 and lin < 10 and col >= 0 and col < 10:

                # verific daca gasesc vreun x
                if self.matr[lin * 10 + col] == 'x':
                    gasitX = 1
                # verific daca gasesc vreun 0
                elif self.matr[lin * 10 + col] == '0':
                    gasit0 = 1

        return gasitX == 1 and gasit0 == 1
    
    def mutari(self, jucator_opus):
        l_mutari = []

        # selectez mai intai toate posibilitatile de piese de forma i,j -> i,j+1
        for i in range(10):
            for j in range(9):
                # verific ca celulele piesei sa fie goale
                if self.matr[i*10+j] == self.__class__.GOL and self.matr[
                    i*10+j+1] == self.__class__.GOL and self.vecini(i,j,i,j+1):
                    matr_tabla_noua = list(self.matr)
                    matr_tabla_noua[i*10+j] = jucator_opus
                    matr_tabla_noua[i * 10 + j + 1] = jucator_opus
                    l_mutari.append(Joc(matr_tabla_noua))

        # selectez toate posibilitatile de piese de forma i+1,j -> i,j
        for i in range(9):
            for j in range(10):
                # verific ca celulele piesei sa fie goale
                if self.matr[i * 10 + j] == self.__class__.GOL and self.matr[
                    (i + 1) * 10 + j] == self.__class__.GOL and self.vecini(i,j,i+1,j):
                    matr_tabla_noua = list(self.matr)
                    matr_tabla_noua[i * 10 + j] = jucator_opus
                    matr_tabla_noua[(i+1) * 10 + j] = jucator_opus
                    l_mutari.append(Joc(matr_tabla_noua))

        return l_mutari

    # linie deschisa inseamna linie pe care jucatorul mai poate forma o configuratie castigatoare
    def linie_deschisa(self, lista, jucator):
        # obtin multimea simbolurilor de pe linie
        mt = set(lista)
        # verific daca sunt maxim 2 simboluri
        if (len(mt) <= 2):
            # daca multimea simbolurilor nu are alte simboluri decat pentru cel de "gol" si jucatorul curent
            if mt <= {self.__class__.GOL, jucator}:
                # inseamna ca linia este deschisa
                return 1
            else:
                return 0
        else:
            return 0

    def linii_deschise(self, jucator):
        rez = 0
        # primul tip de diagonale i,j-> i+1,j+1 -> i+2,j+2
        for i in range(8):
            for j in range(8):
                diagonala = []
                diagonala.append(self.matr[i * 10 + j])
                diagonala.append(self.matr[(i + 1) * 10 + (j + 1)])
                diagonala.append(self.matr[(i + 2) * 10 + (j + 2)])
                rez = rez + self.linie_deschisa(diagonala, jucator)

        # al doilea tip de diagonale i,j-> i-1,j+1 -> i-2,j+2
        for i in range(2, 10):
            for j in range(8):
                diagonala = []
                diagonala.append(self.matr[i * 10 + j])
                diagonala.append(self.matr[(i - 1) * 10 + (j + 1)])
                diagonala.append(self.matr[(i - 2) * 10 + (j + 2)])
                rez = rez + self.linie_deschisa(diagonala, jucator)

        return rez

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        # if (adancime==0):
        if t_final == self.__class__.JMAX:
            return (99 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-99 - adancime)
        elif t_final == 'remiza':
            return 0
        elif self.getScore(self.JMAX) + 10 < self.getScore(self.JMIN): # daca adversarul conduce deja cu cel putin 10 puncte atunci voi incerca sa fac remiza cu el
            return 0
        else: # returnez toate posibilitatile de diagonale care pot aduce puncte pentru playerul JMAX - si scad posibilitatile pe care nu le mai poate face din cauza lui JMIN
            return (self.linii_deschise(self.__class__.JMAX) - self.linii_deschise(self.__class__.JMIN))

    def __str__(self):
        sir = ("X " + " ".join([str(x) for x in range(10)]) + "\n" +
               "0 " + " ".join([str(x) for x in self.matr[0:10]]) + "\n" +
               "1 " + " ".join([str(x) for x in self.matr[10:20]]) + "\n" +
               "2 " + " ".join([str(x) for x in self.matr[20:30]]) + "\n" +
               "3 " + " ".join([str(x) for x in self.matr[30:40]]) + "\n" +
               "4 " + " ".join([str(x) for x in self.matr[40:50]]) + "\n" +
               "5 " + " ".join([str(x) for x in self.matr[50:60]]) + "\n" +
               "6 " + " ".join([str(x) for x in self.matr[60:70]]) + "\n" +
               "7 " + " ".join([str(x) for x in self.matr[70:80]]) + "\n" +
               "8 " + " ".join([str(x) for x in self.matr[80:90]]) + "\n" +
               "9 " + " ".join([str(x) for x in self.matr[90:100]]) + "\n")

        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def jucator_opus(self):
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = self.jucator_opus()
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)
    stare.scor = stare.stare_aleasa.scor
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent < stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if (alpha < stare_noua.scor):
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent > stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if (beta > stare_noua.scor):
                beta = stare_noua.scor
                if alpha >= beta:
                    break
    stare.scor = stare.stare_aleasa.scor

    return stare


def afis_daca_final(stare_curenta,mutari_JMIN,mutari_JMAX):
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat " + final)
            print("Jucatorul " + Joc.JMIN + " are scorul " + str(stare_curenta.tabla_joc.getScore(Joc.JMIN)))
            print("Jucatorul " + Joc.JMAX + " are scorul " + str(stare_curenta.tabla_joc.getScore(Joc.JMAX)))
            print("Jucatorul " + Joc.JMIN + " a facut " + str(mutari_JMIN) + " mutari")
            print("Jucatorul " + Joc.JMAX + " a facut " + str(mutari_JMAX) + " mutari")
        return True

    return False

def main():
    t_inceput = int(round(time.time() * 1000))
    mutari_JMIN = 0
    mutari_JMAX = 0
    if (len(sys.argv) == 1):
        # initializare algoritm
        raspuns_valid = False
        while not raspuns_valid:
            tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
            if tip_algoritm in ['1', '2']:
                raspuns_valid = True
            else:
                print("Nu ati ales o varianta corecta.")

        # initializare jucatori
        raspuns_valid = False
        while not raspuns_valid:
            Joc.JMIN = input("Doriti sa jucati cu x sau cu 0? ").lower()
            if (Joc.JMIN in ['x', '0']):
                raspuns_valid = True
            else:
                print("Raspunsul trebuie sa fie x sau 0.")
        Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'

        # initializare nivel de dificultate
        raspuns_valid = False
        while not raspuns_valid:
            dif = input("Nivel de dificultate? (raspundeti cu 1, 2 sau 3)\n 1.Incepator\n 2.Mediu\n 3.Avansat\n")
            if dif in ['1', '2', '3']:
                raspuns_valid = True
                if dif == '1':
                    ADANCIME_MAX = 2
                elif dif == '2':
                    ADANCIME_MAX = 3
                else:
                    ADANCIME_MAX = 6
            else:
                print("Nu ati ales o varianta corecta.")


        # initializare tabla
        tabla_curenta = Joc()
        print("Tabla initiala")
        print(str(tabla_curenta))

        # creare stare initiala
        stare_curenta = Stare(tabla_curenta, 'x', ADANCIME_MAX)

        while True:

            if (stare_curenta.j_curent == Joc.JMIN):
                t_inainte = int(round(time.time() * 1000))
                # muta jucatorul

                oprire = False
                raspuns_valid = False

                while not raspuns_valid:
                    try:
                        print("Introduceti pozitia piesei")
                        raspuns = input("linie prima celula = ")
                        if raspuns == "exit":
                            # ADDTO
                            # aici trebuie sa afisez scorul utilizatorului si a calculatorul
                            print("Jucatorul " + Joc.JMIN + " are scorul " + stare_curenta.tabla_joc.getScore(Joc.JMIN))
                            print("Jucatorul " + Joc.JMAX + " are scorul " + stare_curenta.tabla_joc.getScore(Joc.JMAX))
                            print("Jucatorul " + Joc.JMIN + " a facut " + mutari_JMIN + " mutari")
                            print("Jucatorul " + Joc.JMAX + " a facut " + mutari_JMAX + " mutari")
                            oprire = True
                            break
                        else:
                            xx = int(raspuns)
                            xy = int(input("coloana prima celula = "))
                            if stare_curenta.tabla_joc.matr[xx * 10 + xy] == Joc.GOL:
                                # daca se poate pune prima celula o cer si pe a doua
                                yx = int(input("linie a doua celula = "))
                                yy = int(input("coloana a doua celula = "))
                                if stare_curenta.tabla_joc.matr[yx * 10 + yy] == Joc.GOL:
                                    if max(xx,yx) - min(xx,yx) + max(xy,yy) - min(xy,yy) == 1:
                                        # daca si a doua se poate pune verific si conditia suplimentara
                                        # daca contine si un x si un 0 pe margine atunci piesa se poate pune

                                        dx = [-1, -1, -1, 0, 0, 1, 1, 1]
                                        dy = [-1, 0, 1, 1, -1, -1, 0, 1]
                                        gasitX = 0
                                        gasit0 = 0
                                        for i in range(8):
                                            lin = dx[i] + xx
                                            col = dy[i] + xy

                                            # verific sa nu ies din matrice
                                            if lin >= 0 and lin < 10 and col >= 0 and col < 10:

                                                # verific daca gasesc vreun x
                                                if stare_curenta.tabla_joc.matr[lin * 10 + col] == 'x':
                                                    gasitX = 1
                                                # verific daca gasesc vreun 0
                                                elif stare_curenta.tabla_joc.matr[lin * 10 + col] == '0':
                                                    gasit0 = 1

                                            lin = dx[i] + yx
                                            col = dy[i] + yy

                                            # verific sa nu ies din matrice
                                            if lin >= 0 and lin < 10 and col >= 0 and col < 10:

                                                # verific daca gasesc vreun x
                                                if stare_curenta.tabla_joc.matr[lin * 10 + col] == 'x':
                                                    gasitX = 1
                                                # verific daca gasesc vreun 0
                                                elif stare_curenta.tabla_joc.matr[lin * 10 + col] == '0':
                                                    gasit0 = 1

                                        if gasitX == 1 and gasit0 == 1:
                                            # dupa iesirea din while sigur am gasit piesa
                                            raspuns_valid = True

                                            # deci pot plasa piesa pe "tabla de joc"
                                            stare_curenta.tabla_joc.matr[xx * 10 + xy] = Joc.JMIN
                                            stare_curenta.tabla_joc.matr[yx * 10 + yy] = Joc.JMIN

                                            # afisarea starii jocului in urma mutarii utilizatorului
                                            print("\nTabla dupa mutarea jucatorului")
                                            print(str(stare_curenta))

                                            mutari_JMIN = mutari_JMIN + 1
                                            # testez daca jocul a ajuns intr-o stare finala
                                            # si afisez un mesaj corespunzator in caz ca da
                                            if (afis_daca_final(stare_curenta,mutari_JMIN,mutari_JMAX)):
                                                break

                                            # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                            stare_curenta.j_curent = stare_curenta.jucator_opus()
                                        else:
                                            print("piesa introdusa nu se poate pune")
                                    else:
                                        print("celulele nu respecta conditia sa fie pe vertical sau orizontal")
                                else:
                                    print("celula dreapta jos nu este libera")
                            else:
                                print("celula stanga sus nu este libera")

                    except ValueError:
                        print("Liniile si coloanele trebuie sa fie numer intreg")

                    if oprire:
                        break
                t_dupa = int(round(time.time() * 1000))
                print("Jucatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            # --------------------------------
            else:  # jucatorul e JMAX (calculatorul)
                # Mutare calculator

                # preiau timpul in milisecunde de dinainte de mutare
                t_inainte = int(round(time.time() * 1000))
                if tip_algoritm == '1':
                    stare_actualizata = min_max(stare_curenta)
                else:  # tip_algoritm==2
                    stare_actualizata = alpha_beta(-500, 500, stare_curenta)
                stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
                print("Tabla dupa mutarea calculatorului")
                print(str(stare_curenta))

                # preiau timpul in milisecunde de dupa mutare
                mutari_JMAX = mutari_JMAX + 1
                t_dupa = int(round(time.time() * 1000))
                print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

                if (afis_daca_final(stare_curenta,mutari_JMIN,mutari_JMAX)):
                    break

                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                stare_curenta.j_curent = stare_curenta.jucator_opus()

        t_final=int(round(time.time() * 1000))
        print("Jocul a durat "+str(t_final-t_inceput)+" milisecunde.")

    elif len(sys.argv) == 2 and sys.argv[1] == "-gui":
        # initializare algoritm
        raspuns_valid = False
        while not raspuns_valid:
            tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
            if tip_algoritm in ['1', '2']:
                raspuns_valid = True
            else:
                print("Nu ati ales o varianta corecta.")

        # initializare jucatori
        raspuns_valid = False
        while not raspuns_valid:
            Joc.JMIN = input("Doriti sa jucati cu x sau cu 0? ").lower()
            if (Joc.JMIN in ['x', '0']):
                raspuns_valid = True
            else:
                print("Raspunsul trebuie sa fie x sau 0.")
        Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'

        # initializare nivel de dificultate
        raspuns_valid = False
        while not raspuns_valid:
            dif = input("Nivel de dificultate? (raspundeti cu 1, 2 sau 3)\n 1.Incepator\n 2.Mediu\n 3.Avansat\n")
            if dif in ['1', '2', '3']:
                raspuns_valid = True
                if dif == '1':
                    ADANCIME_MAX = 2
                elif dif == '2':
                    ADANCIME_MAX = 3
                else:
                    ADANCIME_MAX = 6
            else:
                print("Nu ati ales o varianta corecta.")

        # initializare tabla
        tabla_curenta = Joc()
        print("Tabla initiala")
        print(str(tabla_curenta))

        # creare stare initiala
        stare_curenta = Stare(tabla_curenta, 'x', ADANCIME_MAX)
        pygame.init()
        pygame.display.set_caption('x si zero')
        ecran = pygame.display.set_mode(size=(510, 510))

        patratele = deseneaza_grid(ecran, tabla_curenta.matr)

        xx = xy = yx = yy = 100

        while True:

            if (stare_curenta.j_curent == Joc.JMIN):
                t_inainte = int(round(time.time() * 1000))
                # muta jucatorul

                oprire = False
                raspuns_valid = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        pos = pygame.mouse.get_pos()

                        for np in range(len(patratele)):
                            if patratele[np].collidepoint(pos):
                                linie = np // 10
                                coloana = np % 10

                                if xx == 100 and xy == 100:
                                    xx = linie
                                    xy = coloana
                                    print("celula 1")
                                    print([xx, xy])
                                    if stare_curenta.tabla_joc.matr[xx * 10 + xy] == Joc.GOL:
                                        xx = linie
                                        xy = coloana
                                        # addCell
                                        patratele = deseneaza_gridCell(ecran,
                                                                   stare_curenta.tabla_joc.matr,xx,xy)
                                    else:
                                        xx = xy = 100
                                        print("celula nu este libera")

                                elif yx == 100 and yy == 100:
                                    yx = linie
                                    yy = coloana
                                    print([yx, yy])

                                    if stare_curenta.tabla_joc.matr[yx * 10 + yy] == Joc.GOL:
                                        if max(xx, yx) - min(xx, yx) + max(xy, yy) - min(xy,
                                                                                         yy) == 1:
                                            # daca si a doua se poate pune verific si conditia suplimentara
                                            # daca contine si un x si un 0 pe margine atunci piesa se poate pune

                                            dx = [-1, -1, -1, 0, 0, 1, 1, 1]
                                            dy = [-1, 0, 1, 1, -1, -1, 0, 1]
                                            gasitX = 0
                                            gasit0 = 0
                                            for i in range(8):
                                                lin = dx[i] + xx
                                                col = dy[i] + xy

                                                # verific sa nu ies din matrice
                                                if lin >= 0 and lin < 10 and col >= 0 and col < 10:

                                                    # verific daca gasesc vreun x
                                                    if stare_curenta.tabla_joc.matr[
                                                        lin * 10 + col] == 'x':
                                                        gasitX = 1
                                                    # verific daca gasesc vreun 0
                                                    elif stare_curenta.tabla_joc.matr[
                                                        lin * 10 + col] == '0':
                                                        gasit0 = 1

                                                lin = dx[i] + yx
                                                col = dy[i] + yy

                                                # verific sa nu ies din matrice
                                                if lin >= 0 and lin < 10 and col >= 0 and col < 10:

                                                    # verific daca gasesc vreun x
                                                    if stare_curenta.tabla_joc.matr[
                                                        lin * 10 + col] == 'x':
                                                        gasitX = 1
                                                    # verific daca gasesc vreun 0
                                                    elif stare_curenta.tabla_joc.matr[
                                                        lin * 10 + col] == '0':
                                                        gasit0 = 1

                                            if gasitX == 1 and gasit0 == 1:
                                                print([xx,xy,yx,yy])
                                                # dupa iesirea din while sigur am gasit piesa
                                                raspuns_valid = True

                                                # deci pot plasa piesa pe "tabla de joc"
                                                stare_curenta.tabla_joc.matr[
                                                    xx * 10 + xy] = Joc.JMIN
                                                stare_curenta.tabla_joc.matr[
                                                    yx * 10 + yy] = Joc.JMIN

                                                # afisarea starii jocului in urma mutarii utilizatorului
                                                print("\nTabla dupa mutarea jucatorului")
                                                print(str(stare_curenta))

                                                patratele = deseneaza_grid(ecran,
                                                                           stare_curenta.tabla_joc.matr)

                                                mutari_JMIN = mutari_JMIN + 1
                                                # testez daca jocul a ajuns intr-o stare finala
                                                # si afisez un mesaj corespunzator in caz ca da
                                                if (afis_daca_final(stare_curenta, mutari_JMIN,
                                                                    mutari_JMAX)):
                                                    break

                                                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                                stare_curenta.j_curent = stare_curenta.jucator_opus()

                                                t_dupa = int(round(time.time() * 1000))
                                                print("Jucatorul a \"gandit\" timp de " + str(
                                                    t_dupa - t_inainte) + " milisecunde.")
                                            else:
                                                patratele = deseneaza_grid(ecran,
                                                                           stare_curenta.tabla_joc.matr)
                                                xx = xy = yx = yy = 100
                                                print("piesa introdusa nu se poate pune")
                                        else:
                                            patratele = deseneaza_grid(ecran,
                                                                       stare_curenta.tabla_joc.matr)
                                            xx = xy = yx = yy = 100
                                            print(
                                                "celulele nu respecta conditia sa fie pe vertical sau orizontal")
                                    else:
                                        patratele = deseneaza_grid(ecran,
                                                                   stare_curenta.tabla_joc.matr)
                                        xx = xy = yx = yy = 100
                                        print("celula a doua nu este libera")

            # --------------------------------
            else:  # jucatorul e JMAX (calculatorul)
                # Mutare calculator

                # preiau timpul in milisecunde de dinainte de mutare
                t_inainte = int(round(time.time() * 1000))
                if tip_algoritm == '1':
                    stare_actualizata = min_max(stare_curenta)
                else:  # tip_algoritm==2
                    stare_actualizata = alpha_beta(-500, 500, stare_curenta)
                stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
                print("Tabla dupa mutarea calculatorului")
                print(str(stare_curenta))

                patratele = deseneaza_grid(ecran, stare_curenta.tabla_joc.matr)

                # preiau timpul in milisecunde de dupa mutare
                mutari_JMAX = mutari_JMAX + 1
                t_dupa = int(round(time.time() * 1000))
                print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

                if (afis_daca_final(stare_curenta, mutari_JMIN, mutari_JMAX)):
                    break

                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                stare_curenta.j_curent = stare_curenta.jucator_opus()
                xx = xy = yx = yy = 100

        t_final = int(round(time.time() * 1000))
        print("Jocul a durat " + str(t_final - t_inceput) + " milisecunde.")


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()