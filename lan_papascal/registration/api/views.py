
class SignUp(generics.GenericAPIView):
    serializer_class = UserSignUpSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format = None):
        '''
        Registers user to the server. Input should be in the format:
        '''
        serializer = self.get_serializer(self, data = request.data)

        if serializer.is_valid(): 
           
            serializer.save()

            r = requests.post(f'{BASE_URL}/o/token/', 
                data = {
                    'grant_type': 'password', 
                    'username': request.data['username'], 
                    'password': request.data['password'], 
                    'client_id':settings.CLIENT_ID, 
                    'client_secret': settings.CLIENT_SECRET, 
                }, 
            )

            if not r:
                json = r.json()
                error =  {"errors":{"title":json["errors"]["error"],"detail":json["errors"]["error_handling"], "status": r.status_code}}
                return Response(error,status=r.status_code)

            return Response(r.json(),status=r.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignIn(APIView):
    serializer_class = UserSignInSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format = None):
        '''
        Gets tokens with username/email and password. Input should be in the format:
        {"username": "username", "password": "1234abcd"} 
        or
        {"email":"username@example.com","password":"1234abcd"}
        '''
        serializer = self.get_serializer(self, data = request.data)
        serializer.is_valid(raise_exception=True)

        username = request.POST.get('username', None)
        email = request.POST.get('email', None)

        r = requests.post(f'{BASE_URL}/o/token/', 
            data = {
                'grant_type': 'password', 
                'username': user.username, 
                'password': password, 
                'client_id': settings.CLIENT_ID, 
                'client_secret': settings.CLIENT_SECRET, 
            }, 
        )

        if not r.ok:
            json = r.json()
            error =  {"errors":{"title":json["errors"]["error"],"detail":json["errors"]["error_handling"], "status": r.status_code}}
            return Response(error,status=r.status_code)
        
        return Response(r.json(),status=r.status_code)

class RefreshToken(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format = None):
        '''
        Registers user to the server. Input should be in the format:
        {"token":<token>,"refresh_token": " < refresh_token > "}
        '''
        r = requests.post(
        f'{BASE_URL}/o/token/', 
            data = {
                'grant_type': 'refresh_token', 
                'refresh_token': request.data['refresh_token'], 
                'client_id': settings.CLIENT_ID, 
                'client_secret': settings.CLIENT_SECRET, 
            }, 
        )

        RevokeToken().post(self,request,format)
        return Response(r.json())


class RevokeToken(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format = None):
        '''
        Method to revoke tokens.
        {"token": " < token > "}
        '''
        r = requests.post(
            f'{BASE_URL}/o/revoke_token/', 
            data = {
                'token': request.data['token'], 
                'client_id': settings.CLIENT_ID, 
                'client_secret': settings.CLIENT_SECRET, 
            }, 
        )
        # If it goes well return success message (would be empty otherwise) 
        if r.status_code == request.codes.ok:
            return Response({'message': 'token revoked'}, r.status_code)
        # Return the error if it goes badly
        return Response(r.json(), r.status_code)