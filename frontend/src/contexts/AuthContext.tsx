import React, {
    createContext,
    useContext,
    useState,
    ReactNode,
} from 'react';

import { postLogin } from '../../api/loginService';

import * as SecureStore from 'expo-secure-store';
import { LoginRequest } from '../../api/types';

interface AuthContextType {
    isAuthenticated: boolean;
    isLoading: boolean;
    signIn: (credentials: LoginRequest) => Promise<void>;
    signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(
    undefined
);

interface AuthProviderProps {
    children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const signIn = async (credentials: LoginRequest) => {
        setIsLoading(true);

        try {
            const response = await postLogin(credentials);

            await SecureStore.setItemAsync(
                'access_token',
                response.access_token
            );

            setIsAuthenticated(true);
        } finally {
            setIsLoading(false);
        }
    };

    const signOut = async () => {
        await SecureStore.deleteItemAsync('access_token');
        setIsAuthenticated(false);
    }

    return (
        <AuthContext.Provider
            value={{
                isAuthenticated,
                isLoading,
                signIn,
                signOut
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error(
            'useAuth must be used within an AuthProvider'
        );
    }

    return context;
}