from app.models.user import User, UserRole


class UserFactory:
    """
    Factory Pattern — İstifadəçi yaratmaq üçün fabrika.
    Admin birbaşa User() yaratmaq əvəzinə bu factory-dən istifadə edir.
    Gələcəkdə yeni tip əlavə etsən sadəcə burda dəyişiklik edirsən.
    """

    @staticmethod
    def create_user(
        first_name: str,
        last_name: str,
        email: str,
        role: str
    ) -> User:
        """
        Role-a görə doğru User obyekti yarat.
        Validation da burda həll olunur.
        """
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