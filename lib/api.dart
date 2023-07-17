import 'package:http/http.dart' as http;

Future GetData(url) async{
  return http.get(Uri.parse(url));
  // http.Response Response = await http.get(url);
  // return Response.body;
}