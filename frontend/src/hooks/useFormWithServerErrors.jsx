import { useForm } from 'react-hook-form';
import { toast } from 'react-toastify';

export const useFormWithServerErrors = (options) => {
  const form = useForm(options);
  const { setError, clearErrors, handleSubmit } = form;

  // 1. Calculate Known Fields automatically from defaultValues (or allow override)
  const knownFields = options.knownFields || Object.keys(options.defaultValues || {});

  // 2. The Text Formatter (extracted)
  const formatError = (text) => {
    if (!text) return null;
    return text.split('\\' + 'n').map((line, index) => (
      <span>
        {line}
        {index < text.split('\\' + 'n').length - 1 && <br />} 
      </span>
    ));
  };

  // 3. The Standard Error Handler (Client-side)
  const onClientError = (errors) => {
    console.log("Client-side validation blocked submission:", errors);
    toast.error("Форма містить помилки. Виправте їх перед відправкою.");
  };

  // 4. The Wrapper (Clears errors, then handles submit)
  const wrapSubmit = (submitFn) => {
    return (e) => {
      clearErrors();
      handleSubmit(submitFn, onClientError)(e);
    };
  };

  // 5. The Big Server Error Parser (The main logic chunk)
  const handleServerErrors = (error) => {
    console.error("API Submission Error:", error);

    if (error.response?.data) {
      const serverData = error.response.data;
      let hasFieldErrors = false;

      // Helper to process a single error
      const processError = (fieldName, message) => {
        if (fieldName && knownFields.includes(fieldName)) {
          setError(fieldName, { type: 'server', message: message });
          hasFieldErrors = true;
        } else {
          const displayMsg = fieldName ? `${fieldName}: ${message}` : message;
          toast.error(displayMsg);
          console.error(`Unmapped Error [${fieldName}]:`, message);
        }
      };

      // CHECK 1: Standardized Errors (Array of objects)
      if (Array.isArray(serverData.errors)) {
        serverData.errors.forEach((err) => {
          processError(err.attr, err.detail);
        });
      }
      // CHECK 2: Standard DRF keys (Object)
      else if (typeof serverData === 'object') {
        Object.keys(serverData).forEach((key) => {
          const msg = Array.isArray(serverData[key]) ? serverData[key][0] : serverData[key];
          if (key === 'detail') {
            toast.error(serverData.detail);
          } else {
            processError(key, msg);
          }
        });
      }

      if (hasFieldErrors) {
        toast.error("Перевірте дані форми (помилки підсвічено).");
      } else if (!hasFieldErrors && !serverData.errors) {
        const msg = "Сталася невідома помилка валідації.";
        toast.error(msg);
        console.error(msg, serverData);
      }
    } else {
      const msg = "Сталася помилка сервера або проблема з мережею.";
      toast.error(msg);
      console.error(msg, error);
    }
  };

  return {
    ...form, // Return all standard useForm methods (register, reset, etc.)
    wrapSubmit,
    handleServerErrors,
    formatError,
  };
};