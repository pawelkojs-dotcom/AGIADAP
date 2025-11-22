
Wrzuć pliki z danymi (kolumny: T, rho) do katalogu:
  /mnt/data/LSCO_data
Wymagane nazwy:
  - rho_H0.csv   (H=0 T)
  - rho_H16.csv  (H=16 T)

Opcjonalnie (dla porównania trzech ścieżek):
  - delta_H0.csv  (T, Delta_meV)
  - delta_H16.csv (T, Delta_meV)
  - /mnt/data/LSCO_theta_results.csv (zawiera kolumny T i Theta; jeśli ma H, wybieramy H≈0)

Następnie uruchom ponownie ten skrypt – policzy β_H(T) z transportu,
oszacuje błędy (bootstrap), a figury publication-ready zostaną zaktualizowane.
