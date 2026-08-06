
import inspect
import logging
import random
from time import sleep
from utils.error import messageError
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    ElementNotInteractableException,
    StaleElementReferenceException,
    InvalidElementStateException
)


def _human_typing_delay(min_delay=0.05, max_delay=2):
    """
    Sleep for a random delay to simulate human typing.
    """
    sleep(random.uniform(min_delay, max_delay))


# This function searches for an element on the page, scrolls to it, and writes to it with multiple fallback strategies.
def write_element(driver, element, text, clear=True, slow=False, max_attempts=3):
    # Never log field contents: this helper writes both usernames and passwords.
    input_type = element.get_attribute('type') if element is not None else None
    logging.info(
        "START || %s - Element: %s, Input type: %s, Text length: %s",
        inspect.currentframe().f_code.co_name,
        element,
        input_type,
        len(text) if text is not None else 0,
    )
    """
    Segrating text safely to an element with multiple Fallback strategies

    Args:
        driver: WebDriver de Selenium
        element: Elemento donde escribir
        text: Texto a escribir
        clear: Si limpiar el campo primero (default: True)
        slow: Si escribir carácter por carácter (default: False)
        max_attempts: Número máximo de intentos (default: 3)

    Returns:
        driver: WebDriver actualizado

    Raises:
        messageError: If all writing attempts fail
    """
    try:

        # PASO 1: Try first basic method (Send_keys simple)
        try:

            # Verify that the element is available
            element.is_displayed()

            # Basic scroll to the element
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", element)

            # Basic Actionchainns Con Move_to_Element (Original Method)
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()

            if clear:
                element.clear()

            if slow:
                for char in text:
                    element.send_keys(char)
                    _human_typing_delay()
            else:
                element.send_keys(text)

            # Verify that it was written correctly
            current_value = element.get_attribute('value')
            if current_value and text in current_value:

                return driver
            else:
                logging.debug(
                    "⚠️ Basic method did not verify correctly, moving to advanced methods")

        except (ElementNotInteractableException, InvalidElementStateException, StaleElementReferenceException) as e:
            logging.debug(
                f"⚠️ Basic method failed: {e}, moving to advanced methods")
        except Exception as e:
            logging.debug(
                f"⚠️ Unexpected error in basic method: {e}, moving to advanced methods")

        # PASO 2: If the basic method fails, use advanced methods with make_element_interactable

        for attempt in range(max_attempts):
            try:
                logging.info(
                    f"🔄 Intento avanzado {attempt + 1}/{max_attempts}")

                # Verificar que el elemento sigue siendo válido
                try:
                    element.is_displayed()
                except StaleElementReferenceException:
                    logging.warning(
                        "Elemento obsoleto detectado, saltando intento")
                    continue

                # Scroll al elemento con JavaScript más robusto
                try:
                    driver.execute_script("""
                        arguments[0].scrollIntoView({
                            behavior: 'smooth', 
                            block: 'center',
                            inline: 'center'
                        });
                    """, element)
                    sleep(0.5)
                except Exception as e:
                    logging.warning(f"Error en scroll avanzado: {e}")

                # Habilitar elemento usando make_element_interactable
                make_element_interactable(driver, element)
                sleep(0.2)

                # Método 1: send_keys con ActionChains mejorado
                try:
                    actions = ActionChains(driver)
                    actions.move_to_element(element).perform()
                    sleep(0.1)

                    if clear:
                        element.clear()
                        sleep(0.1)

                    if slow:
                        for char in text:
                            element.send_keys(char)
                            _human_typing_delay()
                    else:
                        element.send_keys(text)

                    current_value = element.get_attribute('value')
                    if current_value and text in current_value:
                        logging.info(
                            "✅ Escritura avanzada con ActionChains exitosa")
                        return driver

                except (ElementNotInteractableException, InvalidElementStateException) as e:
                    logging.debug(f"ActionChains avanzado falló: {e}")

                # Método 2: send_keys directo
                try:
                    if clear:
                        element.clear()
                        sleep(0.1)

                    if slow:
                        for char in text:
                            element.send_keys(char)
                            _human_typing_delay()
                    else:
                        element.send_keys(text)

                    current_value = element.get_attribute('value')
                    if current_value and text in current_value:
                        return driver

                except (ElementNotInteractableException, InvalidElementStateException) as e:
                    logging.debug(f"Send_keys directo avanzado falló: {e}")

                # Método 3: JavaScript para establecer valor
                try:
                    driver.execute_script("""
                        var element = arguments[0];
                        var text = arguments[1];
                        
                        element.value = text;
                        
                        // Disparar eventos
                        var events = ['input', 'change', 'keyup', 'blur'];
                        events.forEach(function(eventType) {
                            var event = new Event(eventType, { bubbles: true, cancelable: true });
                            element.dispatchEvent(event);
                        });
                    """, element, text)

                    current_value = element.get_attribute('value')
                    if current_value and text in current_value:
                        return driver

                except Exception as e:
                    logging.debug(f"JavaScript setValue falló: {e}")

                # Método 4: ActionChains avanzado con limpieza
                try:
                    actions = ActionChains(driver)
                    actions.click(element).perform()
                    sleep(0.2)

                    if clear:
                        actions.key_down(Keys.CONTROL).send_keys(
                            'a').key_up(Keys.CONTROL).perform()
                        sleep(0.1)

                    if slow:
                        for char in text:
                            actions.send_keys(char).perform()
                            _human_typing_delay()
                    else:
                        actions.send_keys(text).perform()

                    current_value = element.get_attribute('value')
                    if current_value and text in current_value:
                        return driver

                except Exception as e:
                    logging.debug(f"ActionChains con limpieza falló: {e}")

                # Método 5: Focus y tipo carácter por carácter
                try:
                    driver.execute_script("arguments[0].focus();", element)
                    sleep(0.1)

                    if clear:
                        driver.execute_script(
                            "arguments[0].value = '';", element)

                    for char in text:
                        element.send_keys(char)
                        if slow:
                            _human_typing_delay()
                        else:
                            sleep(0.01)

                    current_value = element.get_attribute('value')
                    if current_value and text in current_value:
                        return driver

                except Exception as e:
                    logging.debug(f"Focus y tipo carácter falló: {e}")

                # Si llegamos aquí, todos los métodos fallaron en este intento
                logging.warning(
                    f"⚠️ Todos los métodos avanzados fallaron en intento {attempt + 1}")

                if attempt < max_attempts - 1:  # Si no es el último intento
                    sleep(1)  # Esperar antes del siguiente intento

            except StaleElementReferenceException:
                logging.warning(
                    "Elemento obsoleto durante escritura avanzada, continuando...")
                continue
            except Exception as e:
                logging.warning(
                    f"Error inesperado en intento avanzado {attempt + 1}: {e}")
                if attempt < max_attempts - 1:
                    sleep(1)
                continue

        # Si llegamos aquí, todos los intentos fallaron
        logging.error("❌ Todos los intentos de escritura fallaron")
        raise messageError(
            "No se pudo escribir en el elemento después de múltiples intentos")

    except Exception as e:
        raise messageError(
            f"Error {inspect.currentframe().f_code.co_name}: {e}")


def make_element_interactable(driver, element):
    """
    Try to make an interactable element by removing common restrictions

    ARGS:
        Driver: Webdriver of Selenium
        Element: Web element to be interactable

    Returns:
        BOOL: True if the element was successfully enabled
    """
    try:
        logging.debug("Intentando hacer elemento interactuable para escritura")

        # Script para habilitar elemento
        result = driver.execute_script("""
            var element = arguments[0];
            
            try {
                // Quitar atributos restrictivos
                element.removeAttribute('disabled');
                element.removeAttribute('readonly');
                element.disabled = false;
                element.readOnly = false;
                
                // Quitar clases que pueden bloquear interacción
                var restrictiveClasses = [
                    'disabled', 'readonly', 'not-allowed', 'pointer-events-none',
                    'dp__input_readonly', 'dp__pointer', 'dp__disabled'
                ];
                
                restrictiveClasses.forEach(function(className) {
                    element.classList.remove(className);
                });
                
                // Habilitar estilos
                element.style.pointerEvents = 'auto';
                element.style.cursor = 'auto';
                element.style.opacity = '1';
                element.style.visibility = 'visible';
                element.style.display = 'block';
                
                // Si es un input, asegurar que sea de tipo text
                if (element.tagName.toLowerCase() === 'input') {
                    if (element.getAttribute('inputmode') === 'none') {
                        element.setAttribute('inputmode', 'text');
                    }
                    if (!element.type || element.type === 'hidden') {
                        element.setAttribute('type', 'text');
                    }
                }
                
                // Habilitar contenedores padre que puedan estar bloqueando
                var parent = element.parentElement;
                var levels = 0;
                while (parent && levels < 5) {
                    parent.removeAttribute('disabled');
                    parent.disabled = false;
                    parent.style.pointerEvents = 'auto';
                    
                    restrictiveClasses.forEach(function(className) {
                        parent.classList.remove(className);
                    });
                    
                    parent = parent.parentElement;
                    levels++;
                }
                
                return true;
                
            } catch (error) {
                console.error('Error habilitando elemento:', error);
                return false;
            }
        """, element)

        if result:
            logging.debug("Elemento habilitado exitosamente para escritura")
            return True
        else:
            logging.warning("No se pudo habilitar el elemento para escritura")
            return False

    except Exception as e:
        logging.error(f"Error en make_element_interactable: {e}")
        return False
