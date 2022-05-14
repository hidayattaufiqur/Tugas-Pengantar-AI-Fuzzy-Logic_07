import pandas as pd

class Data:
    def baca_data():
        df = pd.read_excel("https://github.com/hidayattaufiqur/Tugas-Pengantar-Fuzzy-Logic_07-/blob/main/bengkel.xlsx?raw=true")
        # df = pd.read_excel("bengkel.xlsx")
        data_bengkel = df.to_dict("records")
        return data_bengkel

    def print_data():
        data = Data.baca_data()
        for i in data:
            print(i)
        print()

    def zip_data(data):
        # TODO: refactor
        fuzzy = Fuzzy()
        zipped_fuzzy = []
        for d in data:
            temp = {"Harga": 0, "Servis": 0}
            temp["Harga"] = fuzzy.harga(d["harga"])
            temp["Servis"] = fuzzy.servis(d["servis"])
            zipped_fuzzy.append(temp)
        return zipped_fuzzy

    def output_data(data):
        peringkat = data[:10]
        df = pd.DataFrame().from_records(peringkat)
        df.to_excel("peringkat.xlsx")


class Fuzzy:
    def servis(self, kualitas):
        metriks = {"Rendah": 0 ,"Sedang": 0, "Tinggi": 0}
        a, b, c, d = 25, 35, 65, 75
        if kualitas <= a:
            metriks["Rendah"] = 1
        if b <= kualitas <= c:
            metriks["Sedang"] = 1
        if kualitas >= d:
            metriks["Tinggi"] = 1
        if a < kualitas <= b: 
            metriks["Rendah"] = (b-kualitas)/(b-a)
        if a < kualitas <= b:
            metriks["Sedang"] = (kualitas-a)/(b-a)
        if c < kualitas <= d:
            metriks["Sedang"] = (d-kualitas)/(d-c)
        if c < kualitas <= d:
            metriks["Tinggi"] = (kualitas-c)/(d-c)
        return metriks
  
    def harga(self, harga):
        metriks = {"Murah": 0, "Sedang": 0, "Mahal": 0}
        a, b, c, d = 2, 4, 6, 8
        if harga <= a:
            metriks["Murah"] = 1
        if b <= harga <= c:
            metriks["Sedang"] = 1
        if harga >= d:
            metriks["Mahal"] = 1
        if a < harga <= b: 
            metriks["Murah"] = (b-harga)/(b-a)
        if a < harga <= b:
            metriks["Sedang"] = (harga-a)/(b-a)
        if c < harga <= d:
            metriks["Sedang"] = (d-harga)/(d-c)
        if c < harga <= d:
            metriks["Mahal"] = (harga-c)/(d-c)
        return metriks


class Inference: 
    def clipping(self, data):
        fuzzy_output = {
            "Tidak Direkomendasikan" : [],
            "Direkomendasikan" : [],
            "Sangat Direkomendasikan" : [],
        }
        # konjungsi
        fuzzy_output["Direkomendasikan"].append(min(data["Harga"]["Murah"], data["Servis"]["Rendah"])) 
        fuzzy_output["Sangat Direkomendasikan"].append(min(data["Harga"]["Murah"], data["Servis"]["Sedang"]))
        fuzzy_output["Sangat Direkomendasikan"].append(min(data["Harga"]["Murah"], data["Servis"]["Tinggi"]))
        fuzzy_output["Tidak Direkomendasikan"].append(min(data["Harga"]["Sedang"], data["Servis"]["Rendah"]))
        fuzzy_output["Direkomendasikan"].append(min(data["Harga"]["Sedang"], data["Servis"]["Sedang"]))
        fuzzy_output["Sangat Direkomendasikan"].append(min(data["Harga"]["Sedang"], data["Servis"]["Tinggi"]))
        fuzzy_output["Tidak Direkomendasikan"].append(min(data["Harga"]["Mahal"], data["Servis"]["Rendah"]))
        fuzzy_output["Direkomendasikan"].append(min(data["Harga"]["Mahal"], data["Servis"]["Sedang"]))
        fuzzy_output["Direkomendasikan"].append(min(data["Harga"]["Mahal"], data["Servis"]["Tinggi"]))
        # disjungsi
        fuzzy_output["Tidak Direkomendasikan"] = max(fuzzy_output["Tidak Direkomendasikan"])
        fuzzy_output["Direkomendasikan"]  = max(fuzzy_output["Direkomendasikan"])
        fuzzy_output["Sangat Direkomendasikan"]  = max(fuzzy_output["Sangat Direkomendasikan"])
        return fuzzy_output


class Defuzzy:
    def sugeno(self, data):
        tidak_direkomendasikan = 40; direkomendasikan = 70; sangat_direkomendasikan = 90
        kualitas = 0; numerator = 0; denominator = 0
        numerator = tidak_direkomendasikan*data["Tidak Direkomendasikan"] + direkomendasikan*data["Direkomendasikan"] + sangat_direkomendasikan*data["Sangat Direkomendasikan"]
        denominator = data["Tidak Direkomendasikan"] + data["Direkomendasikan"] + data["Sangat Direkomendasikan"]
        kualitas = numerator / denominator
        return kualitas
        
if __name__ == '__main__':
    inference = Inference(); defuzzy = Defuzzy(); 
    dt = Data.baca_data(); zipped_data = Data.zip_data(dt)
    kualitas = []
    # proses inferensi dan defuzzifikasi 
    for i in zipped_data:
        kualitas.append(defuzzy.sugeno(inference.clipping(i)))
    idx = 0
    # add kolom kualitas di tiap bengkel
    for row in dt:
        row.update(
            {"kualitas": kualitas[idx]} 
        )
        idx+=1
    # sort data berdasarkan kualitas dan servis (higher better)
    dt.sort(key=lambda x: (x["kualitas"], x["servis"]), reverse=True)
    Data.output_data(dt)
    for row in dt[:10]:
        print(row)