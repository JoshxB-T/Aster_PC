import React, { useState } from 'react';

import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';

import { useRouter } from 'expo-router';
import { useAuth } from '../../contexts/AuthContext';

export default function SettingsScreen() {
    const router = useRouter();

    const {
        isAuthenticated,
        isLoading,
        signOut
    } = useAuth();

    const handleAuthentication = () => {
        if (isAuthenticated) {
            signOut();
        } else {
            router.push('/authentication')
        }
    };

    return (
        <View style={styles.container}>
            <ScrollView
                showsVerticalScrollIndicator={false}
                contentContainerStyle={styles.scrollContent}
              >
                <TouchableOpacity
                    style={[
                        styles.authButton,
                        isAuthenticated && styles.signOutButton,
                        isLoading && styles.disabledButton
                    ]}
                    onPress={handleAuthentication}
                    disabled={isLoading}
                    activeOpacity={0.7}
                >
                    <Text
                        style={styles.authButtonText}
                    >
                        {isAuthenticated ? 'Sign Out' : 'Sign In'}
                    </Text>
                </TouchableOpacity>


                <Text style={styles.footer}>
                    © 2026 AsterPC
                </Text>
            </ScrollView>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F5F7FA',
    },

    scrollContent: {
        paddingHorizontal: 20,
        paddingTop: 15,
        paddingBottom: 35,
    },

    signOutButton: {
        backgroundColor: '#DC2626',
    },

    disabledButton: {
        opacity: 0.5,
    },

    authButton: {
        backgroundColor: '#FF0000',
        padding: 16,
        borderRadius: 10,
        alignItems: 'center',
    },

    authButtonText: {
        color: '#FFFFFF',
        fontSize: 16,
        fontWeight: '600',
    },

    footer: {
        textAlign: 'center',
        fontSize: 12,
        color: '#A0A9B8',
        marginTop: 25,
    },
});
