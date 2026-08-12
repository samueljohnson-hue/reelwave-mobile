import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.samueljohnson.reelwave',
  appName: 'Reelwave',
  webDir: 'www',
  backgroundColor: '#14101c',
  ios: { contentInset: 'automatic' },
  android: { backgroundColor: '#14101c' }
};

export default config;
