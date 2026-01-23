"""
Генератор иллюстраций для книги "РАЗ И НАВСЕГДА"
Использует ComfyUI API с Qwen-Image моделью
"""

import requests
import json
import time
import os
import random
from pathlib import Path

# Обход прокси для локальных подключений
os.environ['NO_PROXY'] = '127.0.0.1,localhost'
os.environ['no_proxy'] = '127.0.0.1,localhost'
if 'http_proxy' in os.environ:
    del os.environ['http_proxy']
if 'https_proxy' in os.environ:
    del os.environ['https_proxy']

# Конфигурация
COMFYUI_URL = "http://127.0.0.1:8190"  # WSL ComfyUI (localhost from WSL)

# Определяем путь в зависимости от ОС
import platform
if platform.system() == "Linux":
    OUTPUT_DIR = Path("/mnt/c/Users/PC/raz-book/images")
else:
    OUTPUT_DIR = Path(r"C:\Users\PC\raz-book\images")
OUTPUT_DIR.mkdir(exist_ok=True)

# Промпты для каждой главы (визуальные концепции без текста)
CHAPTER_PROMPTS = {
    "00": {
        "title": "Prologue - Welcome to the incubator",
        "prompt": "surreal mystical egg floating in cosmic space, cracks with golden light emerging, person silhouette inside translucent eggshell, twilight purple silver atmosphere, spiritual awakening concept, cinematic lighting, photorealistic, 8k",
        "negative": "text, letters, words, anime, cartoon, low quality, blurry"
    },
    "01": {
        "title": "Anatomy of the egg",
        "prompt": "cross-section anatomical diagram of giant cosmic egg, three layers visible: golden yolk center, protective shell, inner membrane, glowing ethereal light, mystical scientific illustration, dark background, detailed textures, photorealistic",
        "negative": "text, letters, labels, anime, cartoon, low quality"
    },
    "02": {
        "title": "Readiness test",
        "prompt": "person standing before giant cracked egg mirror, reflection shows bird ready to hatch, dramatic lighting, surreal dreamscape, purple silver twilight colors, self-discovery concept, cinematic",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "03": {
        "title": "Map of the incubator",
        "prompt": "aerial view of vast egg incubator landscape, countless eggs in various stages of hatching, some cracked some whole, ethereal mist, purple silver light rays, mystical cartography, birds eye view, cinematic",
        "negative": "text, letters, map labels, anime, low quality"
    },
    "04": {
        "title": "Why the shell exists",
        "prompt": "protective eggshell as cosmic shield, meteor shower bouncing off translucent barrier, embryo safely inside, space nebula background, purple violet colors, protection concept, ethereal glow, photorealistic",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "05": {
        "title": "The beak from inside",
        "prompt": "close-up of sharp beak breaking through eggshell from inside, dramatic crack lines radiating outward, golden light pouring through breaks, dark interior, determination concept, macro photography style, intense lighting",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "06": {
        "title": "First crack moment",
        "prompt": "single dramatic crack appearing on giant pristine egg, first ray of golden light breaking through, purple twilight atmosphere, pivotal moment frozen in time, cosmic dust particles, cinematic lighting, photorealistic",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "07": {
        "title": "RAZ as guide - Death as Measure",
        "prompt": "mysterious hooded figure with multiple ethereal eyes, silver-gray robes with purple shimmer, holding scales of balance, standing at cosmic doorway, neither menacing nor kind just precise, twilight atmosphere, mystical psychopomp, photorealistic",
        "negative": "text, letters, anime, skeleton, scary, horror, low quality"
    },
    "08": {
        "title": "Cozy yolk syndrome",
        "prompt": "person curled comfortably in golden glowing yolk, warm amber light, comfortable prison concept, surrounding shell transparent showing stars outside, contrast between comfort and freedom, dreamy atmosphere, photorealistic",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "09": {
        "title": "Fear of cold outside",
        "prompt": "view from inside warm egg looking out through crack at vast cold cosmos, contrast warm golden interior versus dark blue cold exterior, fear and wonder combined, edge of comfort zone, dramatic lighting, photorealistic",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "10": {
        "title": "False cracks - illusion of progress",
        "prompt": "egg with many small decorative cracks that dont penetrate through, surface scratches versus deep fractures, false progress concept, person admiring shallow marks, purple silver lighting, surreal metaphor, photorealistic",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "11": {
        "title": "Morning ritual - checking the shell",
        "prompt": "dawn light illuminating egg from behind person, morning meditation pose, hands touching translucent shell feeling for weak spots, golden sunrise colors through purple twilight, daily practice concept, peaceful awakening, photorealistic",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "12": {
        "title": "Daily strikes - micro-breakthroughs",
        "prompt": "beak making small precise strikes on shell, multiple small cracks accumulating, dust particles floating, determination concept, daily practice visualization, focused energy, dramatic side lighting, photorealistic",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "13": {
        "title": "Evening audit - what cracked today",
        "prompt": "moonlight illuminating egg shell, glowing new cracks from days work, evening reflection, person examining progress, silver purple night atmosphere, peaceful contemplation, photorealistic",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "14": {
        "title": "Crisis protocols - when shell presses",
        "prompt": "person inside egg with walls visibly pressing inward, claustrophobic atmosphere, dramatic lighting showing stress cracks, pressure as catalyst concept, survival mode, intense emotional moment, photorealistic",
        "negative": "text, letters, anime, cartoon, horror, low quality"
    },
    "15": {
        "title": "Working with other eggs - social hatching",
        "prompt": "multiple translucent eggs in proximity, figures visible inside each, some helping others crack, some holding each other back, community of eggs, social dynamics visualization, purple silver atmosphere, photorealistic",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "16": {
        "title": "First steps - wet and naked",
        "prompt": "newly hatched being taking first steps outside broken shell, vulnerable and disoriented but free, wet feathers or membrane, new world stretching ahead, rebirth moment, dawn light, emotional triumph, photorealistic",
        "negative": "text, letters, anime, cartoon, baby chicken, low quality"
    },
    "17": {
        "title": "New shell - cycle continues",
        "prompt": "person who just hatched discovering they are inside larger egg, matryoshka eggs concept, infinite regression, spiral of growth, acceptance of eternal process, cosmic scale, purple silver atmosphere, photorealistic",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "epilogue": {
        "title": "What now - RAZ and ready",
        "prompt": "triumphant figure standing on broken eggshell fragments, looking toward infinite horizon, multiple cracked eggs behind showing journey, future open before them, sunset golden light, completion and new beginning, inspiring, photorealistic",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "cover": {
        "title": "Book cover - hatching instruction",
        "prompt": "dramatic close-up of person breaking through giant eggshell, face emerging through cracks with determination, golden light rays streaming through fractures, purple silver cosmic background, spiritual awakening moment, powerful and inspiring, book cover composition, photorealistic, 8k",
        "negative": "text, letters, words, titles, anime, cartoon, low quality"
    }
}

# ComfyUI workflow template для Qwen-Image
def create_workflow(prompt: str, negative: str, filename: str):
    """Создание workflow для ComfyUI API (формат совместимый с API)"""
    seed = random.randint(1, 2**53)

    # Возвращаем только prompt dict напрямую
    return {
        # VAELoader
        "39": {
            "class_type": "VAELoader",
            "inputs": {
                "vae_name": "qwen_image_vae.safetensors"
            }
        },
        # CLIPLoader
        "38": {
            "class_type": "CLIPLoader",
            "inputs": {
                "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
                "type": "qwen_image",
                "device": "default"
            }
        },
        # UNETLoader
        "37": {
            "class_type": "UNETLoader",
            "inputs": {
                "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors",
                "weight_dtype": "default"
            }
        },
        # LoraLoaderModelOnly (4-step LoRA)
        "73": {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {
                "model": ["37", 0],
                "lora_name": "Qwen-Image-2512-Lightning-4steps-V1.0-bf16.safetensors",
                "strength_model": 1.0
            }
        },
        # ModelSamplingAuraFlow
        "66": {
            "class_type": "ModelSamplingAuraFlow",
            "inputs": {
                "model": ["73", 0],
                "shift": 3.1
            }
        },
        # EmptySD3LatentImage
        "58": {
            "class_type": "EmptySD3LatentImage",
            "inputs": {
                "width": 1328,
                "height": 1328,
                "batch_size": 1
            }
        },
        # CLIPTextEncode (Positive)
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["38", 0],
                "text": prompt
            }
        },
        # CLIPTextEncode (Negative)
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["38", 0],
                "text": negative
            }
        },
        # KSampler
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["66", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["58", 0],
                "seed": seed,
                "steps": 4,
                "cfg": 1.0,
                "sampler_name": "euler",
                "scheduler": "simple",
                "denoise": 1.0
            }
        },
        # VAEDecode
        "8": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["3", 0],
                "vae": ["39", 0]
            }
        },
        # SaveImage
        "60": {
            "class_type": "SaveImage",
            "inputs": {
                "images": ["8", 0],
                "filename_prefix": filename
            }
        }
    }


def queue_prompt(workflow: dict, session: requests.Session) -> str:
    """Отправка workflow в очередь ComfyUI"""
    # ComfyUI API ожидает workflow внутри ключа "prompt"
    payload = {"prompt": workflow}
    response = session.post(
        f"{COMFYUI_URL}/prompt",
        json=payload
    )
    return response.json()


def get_history(prompt_id: str, session: requests.Session) -> dict:
    """Получение результатов генерации"""
    response = session.get(f"{COMFYUI_URL}/history/{prompt_id}")
    return response.json()


def wait_for_completion(prompt_id: str, session: requests.Session, timeout: int = 120):
    """Ожидание завершения генерации"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        history = get_history(prompt_id, session)
        if prompt_id in history:
            return history[prompt_id]
        time.sleep(2)
    raise TimeoutError(f"Generation timeout for {prompt_id}")


def download_image(filename: str, session: requests.Session):
    """Скачивание сгенерированного изображения"""
    response = session.get(f"{COMFYUI_URL}/view", params={
        "filename": filename,
        "type": "output"
    })
    return response.content

# Путь к ComfyUI output в WSL
COMFYUI_OUTPUT = Path("/home/jetmil/comfyui/output")


def generate_chapter_image(chapter_id: str, chapter_data: dict):
    """Генерация изображения для главы"""
    print(f"\n[{chapter_id}] Генерация: {chapter_data['title']}")
    print(f"    Промпт: {chapter_data['prompt'][:80]}...")

    # Создаём сессию без прокси
    session = requests.Session()
    session.trust_env = False  # Важно! Отключаем системные прокси

    # Создаём workflow
    filename = f"chapter_{chapter_id}"
    workflow = create_workflow(
        chapter_data['prompt'],
        chapter_data['negative'],
        filename
    )

    try:
        # Отправляем в очередь
        result = queue_prompt(workflow, session)
        prompt_id = result.get('prompt_id')

        if not prompt_id:
            print(f"    ОШИБКА: Не получен prompt_id")
            if 'error' in result:
                print(f"    Детали: {result['error']}")
            return False

        print(f"    Ожидание генерации (ID: {prompt_id})...")

        # Ждём завершения
        history = wait_for_completion(prompt_id, session)

        # Получаем имя файла из результата
        outputs = history.get('outputs', {})
        for node_id, node_output in outputs.items():
            if 'images' in node_output:
                for img in node_output['images']:
                    img_filename = img['filename']

                    # Скачиваем изображение
                    img_data = download_image(img_filename, session)

                    # Сохраняем локально
                    output_path = OUTPUT_DIR / f"chapter_{chapter_id}.png"
                    with open(output_path, 'wb') as f:
                        f.write(img_data)

                    print(f"    ГОТОВО: {output_path}")
                    return True

        print(f"    ОШИБКА: Изображение не найдено в результатах")
        return False

    except Exception as e:
        print(f"    ОШИБКА: {e}")
        return False


def main():
    print("=" * 60)
    print("Генератор иллюстраций для 'РАЗ И НАВСЕГДА'")
    print("=" * 60)
    print(f"ComfyUI: {COMFYUI_URL}")
    print(f"Выходная папка: {OUTPUT_DIR}")
    print(f"Глав для генерации: {len(CHAPTER_PROMPTS)}")
    print("=" * 60)

    # Проверяем доступность ComfyUI
    session = requests.Session()
    session.trust_env = False

    try:
        response = session.get(f"{COMFYUI_URL}/system_stats", timeout=5)
        if response.status_code != 200:
            print("ОШИБКА: ComfyUI недоступен!")
            print("Запустите ComfyUI в WSL: cd ~/comfyui && python main.py --listen 0.0.0.0 --port 8190")
            return
        print("ComfyUI доступен!")
    except Exception as e:
        print(f"ОШИБКА подключения к ComfyUI: {e}")
        print("Запустите ComfyUI в WSL: cd ~/comfyui && python main.py --listen 0.0.0.0 --port 8190")
        return

    success = 0
    failed = 0

    for chapter_id, chapter_data in CHAPTER_PROMPTS.items():
        if generate_chapter_image(chapter_id, chapter_data):
            success += 1
        else:
            failed += 1

        # Небольшая пауза между генерациями
        time.sleep(2)

    print("\n" + "=" * 60)
    print(f"ИТОГО: {success} успешно, {failed} ошибок")
    print("=" * 60)


if __name__ == "__main__":
    main()
