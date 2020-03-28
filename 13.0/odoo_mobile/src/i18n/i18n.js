import I18n from 'i18n-js';
import en from './locales/en';
import vi from './locales/vi';
import es from './locales/es';

I18n.fallbacks = true;

I18n.translations = {
  en,
  vi,
  es
};

export default I18n;
