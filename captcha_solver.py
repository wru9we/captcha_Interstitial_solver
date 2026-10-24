import asyncio
import os


from dotenv import load_dotenv
from patchright.async_api import async_playwright
from playwright_captcha import CaptchaType, ClickSolver, FrameworkType

load_dotenv()



VFS_URL = os.getenv('VFS_URL')
MAX_RETRIES = int(os.getenv('MAX_RETRIES'))
HEADLESS = os.getenv('HEADLESS', 'False') in ('True')



async def solve_captcha():
    for attempt in range(1, MAX_RETRIES + 1):
        print(f'\nпопытка {attempt} из {MAX_RETRIES}')

        try:
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(
                    channel='chrome',
                    headless=HEADLESS,
                )
                context = await browser.new_context(
                    viewport={'width': 1366, 'height': 768},
                    locale='ru-RU',
                )
                page = await context.new_page()

                framework = FrameworkType.PATCHRIGHT

                async with ClickSolver(framework=framework, page=page) as solver:
                    print(f'Открываем {VFS_URL}')
                    await page.goto(VFS_URL)
                    await asyncio.sleep(3)


                    await solver.solve_captcha(
                        captcha_container=page,
                        captcha_type=CaptchaType.CLOUDFLARE_INTERSTITIAL,
                    )



                await asyncio.sleep(10)
                await browser.close()

                return {'success': True, 'message': 'Капча успешно пройдена!'}

        except Exception as e:
            print(f'!Ошибка: {e}')

        if attempt < MAX_RETRIES:
            wait_time = attempt * 5
            print(f'Ждём {wait_time} секунд перед следующей попыткой')
            await asyncio.sleep(wait_time)

    return {'success': False, 'message': 'Не удалось пройти капчу'}


if __name__ == '__main__':
    result = asyncio.run(solve_captcha())
    print(f'\nРезультат: {result["message"]}')
