export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'ADMIN' | 'MANAGER' | 'EMPLOYEE';
  phone_number: string;
  is_active: boolean;
  created_at: string;
}

export interface JwtTokens {
  access: string;
  refresh: string;
}

export interface AuthData {
  user: User;
  tokens: JwtTokens;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone_number?: string;
  password: string;
  password_confirm: string;
}

