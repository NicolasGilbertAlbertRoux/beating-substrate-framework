# Beating Substrate Framework (BST)

**Une ré-organisation géométrique, sur-déterminée et honnêtement auditée des fondements de la physique établie — *non* une théorie du tout.**

Dépôt : <https://github.com/NicolasGilbertAlbertRoux/beating-substrate-framework>

---

## En une phrase

À partir d'un unique objet géométrique — le gradient de phase ∇θ d'un substrat *battant* porté à sa criticité — et de quatre axiomes ontologiques, une chaîne de constructions numériques **réorganise** les fondements de la physique connue (électrostatique, criticité KT, structure quantique, cinématique relativiste, masse, gravité jusqu'à Newton et l'Einstein conique 2+1, contenu de représentation de la matière), chaque étape étant pré-enregistrée, contrôlée, et étiquetée par son statut honnête.

## Ce que ce projet est — et n'est pas

- **C'est** une ré-description cohérente, *sur-contrainte dans sa catégorie forcée* (≈10 résultats sans paramètre pour ≈6 boutons continus), honorant à chaque pas la physique existante.
- **Ce n'est pas** une théorie du tout : le cadre ne réduit pas le nombre de paramètres libres sous celui du Modèle Standard, et ne prédit ni les masses, ni les groupes de jauge, ni les magnitudes de G et de Λ. Ces limites sont **nommées explicitement**, jamais cachées.

## L'ensemble d'axiomes (forme finale)

- **Socle (I–IV)** — objet minimal battant + dimensions ; crénelage (observable/latent par la résolution) ; mouvement par action-rétroaction / cycle ; strates latentes. *Posé (ontologie de départ).*
- **[R1]** Substrat = algèbre géométrique de l'espace-temps, le battement étant le mode conservatif grade-0 à *c*. *Affine le socle I/III* → donne l'opérateur de Dirac 3+1 (exact) et, sous identification naturelle, les ondes gravitationnelles à *c* (γ=1).
- **[R2]** Criticité + verrouillage cyclique. *Affine le socle II* → domaine des structures internes.
- **[P1]** Couleur Z₃ — *posé*, logé dans le latent ; sa dérivation depuis un triplet de directions est interdite par un théorème (Coleman-Mandula).
- **[P2]** Générations par **seuil de résolution** — *posé* (le seuil tombe entre le 3ᵉ et le 4ᵉ verrou cyclique) ; prédit des générations supplémentaires sous le seuil.
- **Magnitudes (masses, G, Λ) — cartographiées** : unifiées en ontologie (trois projections d'un même substrat) ; tout coefficient de fermeture *forcé* (point fixe du flux de Kosterlitz–Thouless, 2/π) ; reste un **unique datum off-critique** (le couplage relevant nu = le problème hiérarchie / constante cosmologique, ouvert pour *toute* la physique ; catastrophe Λ déjà levée). **Adoptés** : ℏ (constante mesurée), règle de Born.

Le seul mur véritablement irréductible est méta-théorique : toute théorie finit sur des axiomes posés.

## Structure du dépôt

```
scripts/        stageN_*.py — une étape numérique par fichier, autonome et pré-enregistrée
                tool_basin_hopping_clusters.py — outil de diagnostic (Stages 15–17), à lancer à part
reproduce.py    exécute tous les stages dans l'ordre et rapporte un résumé pass/échec
ARTICLE_substrat_battant.md / .pdf   l'article (base complète, à retravailler avec des pairs humains)
RECUEIL_propositions.tex / .pdf      le recueil des propositions, avec statut de chacune
CHARTER.md      la charte : statut honnête (forcé / conditionnel / adopté / ouvert) de chaque étape
SOCLE_ontologique.md   le socle ontologique en standalone (optionnel ; redondant avec l'article §2)
requirements.txt       dépendances Python (numpy, scipy, scikit-learn)
LICENSE         MIT
```

## Reproduire

```bash
python reproduce.py            # exécute tous les stages
python reproduce.py --quiet    # résumé seul
python reproduce.py 34 41      # seulement les stages 34 et 41
```

**Prérequis** : Python 3.10+, NumPy, SciPy (scikit-learn pour quelques stages précoces). Les scripts sont autonomes et déterministes. Note : `np.trapz` a été renommé `np.trapezoid` dans les NumPy récents.

## Méthodologie (le cœur honnête)

Chaque étape **pré-enregistre** son observable et son hypothèse nulle *avant* exécution, inclut des **contrôles négatifs** (graphes aléatoires, mélanges, limites de symétrie), traite le battement comme une dynamique *interne conservant l'énergie* (intégration symplectique), et reporte ses artefacts numériques après raffinement. On ne compte comme **signal** que le *sur-déterminé* (résultats forcés sans paramètre) ; les structures *importées* (re-descriptions de modèles établis) ne comptent pas comme preuve. Aucun résultat fonctionnel n'est présenté comme une mesure de la nature.

## Citer / remercier

Travail mené par **Nicolas Roux**, dans un esprit fédératif et de respect des pairs (Madelung, Kosterlitz-Thouless, de Broglie, Sakharov, Dirac, Weinberg-Deser, Kleinert, énergie sombre holographique, et autres), avec assistance computationnelle. Une base complète, destinée à être retravaillée avec des mathématiciens et physiciens humains.

## Licence

MIT — voir [LICENSE](LICENSE).
