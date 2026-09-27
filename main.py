## Jhoan Sebastian Fernandez

from collections import defaultdict
import threading
import random

#  FASE MAP aqui se procesa cada subconjunto de imagenes
def map(image_chunk, results, index):
    "cada hilo procesa una lista de imagens (id_imagen, matriz_pixeles) y les calcula el brillo promedio para luego"
    "clasificarlas."
    local_classification = defaultdict(list)
    
    for img_id, pixel_matrix in image_chunk:
        total_pixels = sum(len(row) for row in pixel_matrix)
        sum_intensity = sum(sum(row) for row in pixel_matrix)
        avg_brightness = sum_intensity / total_pixels if total_pixels > 0 else 0

        label = "CLARA" if avg_brightness >= 128 else "OSCURA"
        local_classification[label].append((img_id, round(avg_brightness, 2)))
    results[index] = dict(local_classification)

#  FASE REDUCE aqui la clasificación de las imagenes se consolida
def reduce(mapped_results):
    global_classification = defaultdict(list)
    
    for local_map in mapped_results:
        for label, img_list in local_map.items():
            global_classification[label].extend(img_list)
                
    return dict(global_classification)

def main(image_batch):
    num_sections = 4  # Número de hilos
    section_size = len(image_batch)
 
    sections = [image_batch[i * section_size:(i + 1) * section_size] for i in range(num_sections)]

    if len(image_batch) % num_sections != 0:
        sections[-1].extend(image_batch[num_sections * section_size:])

    threads = []
    results = [None] * len(sections)

    for i, section in enumerate(sections):
        thread = threading.Thread(target=map, args=(section, results, i))
        threads.append(thread)
        thread.start()

    # Se espera a que los hilos terminen
    for thread in threads:
        thread.join()

    final_result = reduce(results)
    return final_result

if __name__ == "__main__":
    # Generación random del lote de imagénes
    num_imagenes = 20
    batch = []

    for i in range(1, num_imagenes + 1):
        matriz_pixeles = [[random.randint(0, 255) for _ in range(4)] for _ in range(4)]
        batch.append((f"IMG_{i:03d}.png", matriz_pixeles))

    reporte = main(batch)
    
    print("Sistema de procesamiento de imagenes")
    for categoria, lista_imgs in reporte.items():
        print(f"\nCategoría [{categoria}]: {len(lista_imgs)} imágenes")
        for img_id, brillo in lista_imgs:
            print(f"  - {img_id} (Brillo promedio: {brillo})")