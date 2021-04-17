from erToAFNe import erToAFNe
from afneToAFN import afneToAFN
from afnToAFD import afnToAFD
from afdToAFDmin import afdToAFDmin
from classes import ER
from classes import AFD
from classes import AFN

er = ER(".(+(a, b), c)")

afne = erToAFNe(er)

afne.printar()

afn = afneToAFN(afne)

afn.printar()

afd = afnToAFD(afn)

afd.printar()

afdm = afdToAFDmin(afd)

afdm.printar()



