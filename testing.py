from features import Adventure

if __name__ == "__main__":
    # Adventure.adventureZone('grb')
    zones = ""
    for z in Adventure.zones.keys():
        zones += z + " "
    print(zones)
