from app.models.user import User, UserRole


class UserFactory:
    """
    Factory Pattern
    birbaşa User() yaratmaq əvəzinə bu factory-dən istifadə
    Gələcəkdə yeni tip əlavə etsən burda et
    """

    @staticmethod
    def create_user(
        first_name: str,
        last_name: str,
        email: str,
        role: str
    ) -> User:

        role_map = {
            "student": UserRole.STUDENT,
            "teacher": UserRole.TEACHER,
        }

        if role.lower() not in role_map:
            raise ValueError(f"Yanlış rol: '{role}'. 'student' və ya 'teacher' olmalıdır")

        user = User(
            first_name = first_name,
            last_name = last_name,
            email = email,
            role = role_map[role.lower()]
        )

        return user