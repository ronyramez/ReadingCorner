import "dotenv/config";

export default {
  expo: {
    name: "ReadingCorner",
    slug: "ReadingCorner",
    version: "1.0.0",
    orientation: "portrait",
    icon: "./assets/images/icon.png",
    scheme: "ReadingCorner",
    userInterfaceStyle: "automatic",
    splash: {
      image: "./assets/images/splash.png",
      resizeMode: "contain",
      backgroundColor: "#ffffff",
    },
    updates: {
      enabled: true,
      checkAutomatically: "ON_LOAD",
      fallbackToCacheTimeout: 0,
    },
    ios: {
      usesAppleSignIn: true,
      supportsTablet: true,
    },
    android: {
      package: "com.ReadingCorner.project",
      adaptiveIcon: {
        foregroundImage: "./assets/images/adaptive-icon.png",
        backgroundColor: "#ffffff",
      },
    },
    web: {
      bundler: "metro",
      output: "static",
      favicon: "./assets/images/favicon.png",
    },
    plugins: ["expo-router", "expo-secure-store"],
    experiments: {
      typedRoutes: true,
    },
    extra: {
      supabaseUrl: process.env.REACT_NATIVE_SUPABASE_URL,
      supabaseAnonKey: process.env.REACT_NATIVE_SUPABASE_ANON_KEY,
    },
  },
};
