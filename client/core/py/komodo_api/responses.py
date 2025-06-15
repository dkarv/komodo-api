from .types import *
from abc import ABC, abstractmethod
from typing import overload

Res = TypeVar('Res')

class AuthApi(ABC):

  @abstractmethod
  def _auth(self, request: AuthRequest) -> Res: pass

  def auth(self, params: GetLoginOptions) -> GetLoginOptionsResponse:
    return self.auth(AuthRequestGetLoginOptions(params = params), GetLoginOptionsResponse)
  def auth(self, params: CreateLocalUser) -> CreateLocalUserResponse:
    return self.auth(AuthRequestCreateLocalUser(params = params), CreateLocalUserResponse)
  def auth(self, params: LoginLocalUser) -> LoginLocalUserResponse: 
    return self.auth(AuthRequestLoginLocalUser(params = params), LoginLocalUserResponse)
  def auth(self, params: ExchangeForJwt) -> ExchangeForJwtResponse:
    return self.auth(AuthRequestExchangeForJwt(params = params), ExchangeForJwtResponse)
  def auth(self, params: GetUser) -> GetUserResponse:
    return self._auth(AuthRequestGetUser(params = params), GetUserResponse)


class UserResponses: pass
class PushRecentlyViewed(UserResponses, PushRecentlyViewedResponse): pass
class SetLastSeenUpdate(UserResponses, SetLastSeenUpdateResponse): pass
class CreateApiKey(UserResponses, CreateApiKeyResponse): pass
class DeleteApiKey(UserResponses, DeleteApiKeyResponse): pass



class ReadResponses: pass

class GetVersion(ReadResponses, GetVersionResponse): pass
class GetCoreInfo(ReadResponses, GetCoreInfoResponse): pass
class ListSecrets(ReadResponses, ListSecretsResponse): pass
class ListGitProvidersFromConfig(ReadResponses, ListGitProvidersFromConfigResponse): pass
class ListDockerRegistriesFromConfig(ReadResponses, ListDockerRegistriesFromConfigResponse): pass

# ==== USER ====
class GetUsername(ReadResponses, GetUsernameResponse): pass
class GetPermission(ReadResponses, GetPermissionResponse): pass
class FindUser(ReadResponses, FindUserResponse): pass
class ListUsers(ReadResponses, ListUsersResponse): pass
class ListApiKeys(ReadResponses, ListApiKeysResponse): pass
class ListApiKeysForServiceUser(ReadResponses, ListApiKeysForServiceUserResponse): pass
class ListPermissions(ReadResponses, ListPermissionsResponse): pass
class ListUserTargetPermissions(ReadResponses, ListUserTargetPermissionsResponse): pass

# ==== USER GROUP ====
class GetUserGroup(ReadResponses, GetUserGroupResponse): pass
class ListUserGroups(ReadResponses, ListUserGroupsResponse): pass

# ==== PROCEDURE ====
class GetProceduresSummary(ReadResponses, GetProceduresSummaryResponse): pass
class GetProcedure(ReadResponses, GetProcedureResponse): pass
class GetProcedureActionState(ReadResponses, GetProcedureActionStateResponse): pass
class ListProcedures(ReadResponses, ListProceduresResponse): pass
class ListFullProcedures(ReadResponses, ListFullProceduresResponse): pass

# ==== ACTION ====
class GetActionsSummary(ReadResponses, GetActionsSummaryResponse): pass
class GetAction(ReadResponses, GetActionResponse): pass
class GetActionActionState(ReadResponses, GetActionActionStateResponse): pass
class ListActions(ReadResponses, ListActionsResponse): pass
class ListFullActions(ReadResponses, ListFullActionsResponse): pass

# ==== SCHEDULE ====
class ListSchedules(ReadResponses, ListSchedulesResponse): pass

# ==== SERVER ====
class GetServersSummary(ReadResponses, GetServersSummaryResponse): pass
class GetServer(ReadResponses, GetServerResponse): pass
class GetServerState(ReadResponses, GetServerStateResponse): pass
class GetPeripheryVersion(ReadResponses, GetPeripheryVersionResponse): pass
class GetDockerContainersSummary(ReadResponses, GetDockerContainersSummaryResponse): pass
class ListDockerContainers(ReadResponses, ListDockerContainersResponse): pass
class ListAllDockerContainers(ReadResponses, ListAllDockerContainersResponse): pass
class InspectDockerContainer(ReadResponses, InspectDockerContainerResponse):pass
class GetResourceMatchingContainer(ReadResponses, GetResourceMatchingContainerResponse): pass
class GetContainerLog(ReadResponses, GetContainerLogResponse): pass
class SearchContainerLog(ReadResponses, SearchContainerLogResponse): pass
class ListDockerNetworks(ReadResponses, ListDockerNetworksResponse): pass
class InspectDockerNetwork(ReadResponses, InspectDockerNetworkResponse): pass
class ListDockerImages(ReadResponses, ListDockerImagesResponse): pass
class InspectDockerImage(ReadResponses, InspectDockerImageResponse): pass
class ListDockerImageHistory(ReadResponses, ListDockerImageHistoryResponse): pass
class ListDockerVolumes(ReadResponses, ListDockerVolumesResponse): pass
class InspectDockerVolume(ReadResponses, InspectDockerVolumeResponse): pass
class ListComposeProjects(ReadResponses, ListComposeProjectsResponse): pass
class GetServerActionState(ReadResponses, GetServerActionStateResponse): pass
class GetHistoricalServerStats(ReadResponses, GetHistoricalServerStatsResponse): pass
class ListServers(ReadResponses, ListServersResponse): pass
class ListFullServers(ReadResponses, ListFullServersResponse): pass
class ListTerminals(ReadResponses, ListTerminalsResponse): pass

# ==== STACK ====
class GetStacksSummary(ReadResponses, GetStacksSummaryResponse): pass
class GetStack(ReadResponses, GetStackResponse): pass
class GetStackActionState(ReadResponses, GetStackActionStateResponse): pass
class GetStackWebhooksEnabled(ReadResponses, GetStackWebhooksEnabledResponse): pass
class GetStackLog(ReadResponses, GetStackLogResponse): pass
class SearchStackLog(ReadResponses, SearchStackLogResponse): pass
class InspectStackContainer(ReadResponses, InspectStackContainerResponse): pass
class ListStacks(ReadResponses, ListStacksResponse): pass
class ListFullStacks(ReadResponses, ListFullStacksResponse): pass
class ListStackServices(ReadResponses, ListStackServicesResponse): pass
class ListCommonStackExtraArgs(ReadResponses, ListCommonStackExtraArgsResponse): pass
class ListCommonStackBuildExtraArgs(ReadResponses, ListCommonStackBuildExtraArgsResponse): pass

  # ==== DEPLOYMENT ====
class GetDeploymentsSummary(ReadResponses, GetDeploymentsSummaryResponse): pass
class GetDeployment(ReadResponses, GetDeploymentResponse): pass
class GetDeploymentContainer(ReadResponses, GetDeploymentContainerResponse): pass
class GetDeploymentActionState(ReadResponses, GetDeploymentActionStateResponse): pass
class GetDeploymentStats(ReadResponses, GetDeploymentStatsResponse): pass
class GetDeploymentLog(ReadResponses, GetDeploymentLogResponse): pass
class SearchDeploymentLog(ReadResponses, SearchDeploymentLogResponse): pass
class InspectDeploymentContainer(ReadResponses, InspectDeploymentContainerResponse): pass
class ListDeployments(ReadResponses, ListDeploymentsResponse): pass
class ListFullDeployments(ReadResponses, ListFullDeploymentsResponse): pass
class ListCommonDeploymentExtraArgs(ReadResponses, ListCommonDeploymentExtraArgsResponse): pass

  # ==== BUILD ====
class GetBuildsSummary(ReadResponses, GetBuildsSummaryResponse): pass
class GetBuild(ReadResponses, GetBuildResponse): pass
class GetBuildActionState(ReadResponses, GetBuildActionStateResponse): pass
class GetBuildMonthlyStats(ReadResponses, GetBuildMonthlyStatsResponse): pass
class GetBuildWebhookEnabled(ReadResponses, GetBuildWebhookEnabledResponse): pass
class ListBuilds(ReadResponses, ListBuildsResponse): pass
class ListFullBuilds(ReadResponses, ListFullBuildsResponse): pass
class ListBuildVersions(ReadResponses, ListBuildVersionsResponse): pass
class ListCommonBuildExtraArgs(ReadResponses, ListCommonBuildExtraArgsResponse): pass

  # ==== REPO ====
class GetReposSummary(ReadResponses, GetReposSummaryResponse): pass
class GetRepo(ReadResponses, GetRepoResponse): pass
class GetRepoActionState(ReadResponses, GetRepoActionStateResponse): pass
class GetRepoWebhooksEnabled(ReadResponses, GetRepoWebhooksEnabledResponse): pass
class ListRepos(ReadResponses, ListReposResponse): pass
class ListFullRepos(ReadResponses, ListFullReposResponse): pass

  # ==== SYNC ====
class GetResourceSyncsSummary(ReadResponses, GetResourceSyncsSummaryResponse): pass
class GetResourceSync(ReadResponses, GetResourceSyncResponse): pass
class GetResourceSyncActionState(ReadResponses, GetResourceSyncActionStateResponse): pass
class GetSyncWebhooksEnabled(ReadResponses, GetSyncWebhooksEnabledResponse): pass
class ListResourceSyncs(ReadResponses, ListResourceSyncsResponse): pass
class ListFullResourceSyncs(ReadResponses, ListFullResourceSyncsResponse): pass

  # ==== BUILDER ====
class GetBuildersSummary(ReadResponses, GetBuildersSummaryResponse): pass
class GetBuilder(ReadResponses, GetBuilderResponse): pass
class ListBuilders(ReadResponses, ListBuildersResponse): pass
class ListFullBuilders(ReadResponses, ListFullBuildersResponse): pass

  # ==== ALERTER ====
class GetAlertersSummary(ReadResponses, GetAlertersSummaryResponse): pass
class GetAlerter(ReadResponses, GetAlerterResponse): pass
class ListAlerters(ReadResponses, ListAlertersResponse): pass
class ListFullAlerters(ReadResponses, ListFullAlertersResponse): pass

  # ==== TOML ====
class ExportAllResourcesToToml(ReadResponses, ExportAllResourcesToTomlResponse): pass
class ExportResourcesToToml(ReadResponses, ExportResourcesToTomlResponse): pass

  # ==== TAG ====
class GetTag(ReadResponses, GetTagResponse): pass
class ListTags(ReadResponses, ListTagsResponse): pass

  # ==== UPDATE ====
class GetUpdate(ReadResponses, GetUpdateResponse): pass
class ListUpdates(ReadResponses, ListUpdatesResponse): pass

  # ==== ALERT ====
class ListAlerts(ReadResponses, ListAlertsResponse): pass
class GetAlert(ReadResponses, GetAlertResponse): pass

  # ==== SERVER STATS ====
class GetSystemInformation(ReadResponses, GetSystemInformationResponse): pass
class GetSystemStats(ReadResponses, GetSystemStatsResponse): pass
class ListSystemProcesses(ReadResponses, ListSystemProcessesResponse): pass

  # ==== VARIABLE ====
class GetVariable(ReadResponses, GetVariableResponse): pass
class ListVariables(ReadResponses, ListVariablesResponse): pass

  # ==== PROVIDER ====
class GetGitProviderAccount(ReadResponses, GetGitProviderAccountResponse): pass
class ListGitProviderAccounts(ReadResponses, ListGitProviderAccountsResponse): pass
class GetDockerRegistryAccount(ReadResponses, GetDockerRegistryAccountResponse): pass
class ListDockerRegistryAccounts(ReadResponses, ListDockerRegistryAccountsResponse): pass



class WriteResponses: pass

# ==== USER ====
class  UpdateUserUsername(WriteResponses, UpdateUserUsername): pass
class  UpdateUserPassword(WriteResponses, UpdateUserPassword): pass
class  DeleteUser(WriteResponses, DeleteUser): pass

  # ==== SERVICE USER ====
class  CreateServiceUser(WriteResponses, CreateServiceUserResponse): pass
class  UpdateServiceUserDescription(WriteResponses, UpdateServiceUserDescriptionResponse): pass
class  CreateApiKeyForServiceUser(WriteResponses, CreateApiKeyForServiceUserResponse): pass
class  DeleteApiKeyForServiceUser(WriteResponses, DeleteApiKeyForServiceUserResponse): pass

  # ==== USER GROUP ====
class  CreateUserGroup(WriteResponses, UserGroup): pass
class  RenameUserGroup(WriteResponses, UserGroup): pass
class  DeleteUserGroup(WriteResponses, UserGroup): pass
class  AddUserToUserGroup(WriteResponses, UserGroup): pass
class  RemoveUserFromUserGroup(WriteResponses, UserGroup): pass
class  SetUsersInUserGroup(WriteResponses, UserGroup): pass
class  SetEveryoneUserGroup(WriteResponses, UserGroup): pass

  # ==== PERMISSIONS ====
class  UpdateUserAdmin(WriteResponses, UpdateUserAdminResponse): pass
class  UpdateUserBasePermissions(WriteResponses, UpdateUserBasePermissionsResponse): pass
class  UpdatePermissionOnResourceType(WriteResponses, UpdatePermissionOnResourceTypeResponse): pass
class  UpdatePermissionOnTarget(WriteResponses, UpdatePermissionOnTargetResponse): pass

  # ==== DESCRIPTION ====
class  UpdateDescription(WriteResponses, UpdateDescriptionResponse): pass

  # ==== SERVER ====
class  CreateServer(WriteResponses, Server): pass
class  DeleteServer(WriteResponses, Server): pass
class UpdateServer(WriteResponses, Server): pass
class  RenameServer(WriteResponses, Update): pass
class  CreateNetwork(WriteResponses, Update): pass
class  CreateTerminal(WriteResponses, NoData): pass
class  DeleteTerminal(WriteResponses, NoData): pass
class  DeleteAllTerminals(WriteResponses, NoData): pass

  # ==== STACK ====
class  CreateStack(WriteResponses, Stack): pass
class  CopyStack(WriteResponses, Stack): pass
class  DeleteStack(WriteResponses, Stack): pass
class  UpdateStack(WriteResponses, Stack): pass
class  RenameStack(WriteResponses, Update): pass
class  WriteStackFileContents(WriteResponses, Update): pass
class  RefreshStackCache(WriteResponses, NoData): pass
class  CreateStackWebhook(WriteResponses, CreateStackWebhookResponse): pass
class  DeleteStackWebhook(WriteResponses, DeleteStackWebhookResponse): pass

  # ==== DEPLOYMENT ====
class  CreateDeployment(WriteResponses, Deployment): pass
class  CopyDeployment(WriteResponses, Deployment): pass
class  CreateDeploymentFromContainer(WriteResponses, Deployment): pass
class  DeleteDeployment(WriteResponses, Deployment): pass
class  UpdateDeployment(WriteResponses, Deployment): pass
class  RenameDeployment(WriteResponses, Update): pass

  # ==== BUILD ====
class  CreateBuild(WriteResponses, Build): pass
class  CopyBuild(WriteResponses, Build): pass
class  DeleteBuild(WriteResponses, Build): pass
class  UpdateBuild(WriteResponses, Build): pass
class  RenameBuild(WriteResponses, Update): pass
class  WriteBuildFileContents(WriteResponses, Update): pass
class  RefreshBuildCache(WriteResponses, NoData): pass
class  CreateBuildWebhook(WriteResponses, CreateBuildWebhookResponse): pass
class  DeleteBuildWebhook(WriteResponses, DeleteBuildWebhookResponse): pass

  # ==== BUILDER ====
class  CreateBuilder(WriteResponses, Builder): pass
class  CopyBuilder(WriteResponses, Builder): pass
class  DeleteBuilder(WriteResponses, Builder): pass
class  UpdateBuilder(WriteResponses, Builder): pass
class  RenameBuilder(WriteResponses, Update): pass

  # ==== REPO ====
class  CreateRepo(WriteResponses, Repo): pass
class  CopyRepo(WriteResponses, Repo): pass
class  DeleteRepo(WriteResponses, Repo): pass
class  UpdateRepo(WriteResponses, Repo): pass
class  RenameRepo(WriteResponses, Update): pass
class  RefreshRepoCache(WriteResponses, NoData): pass
class  CreateRepoWebhook(WriteResponses, CreateRepoWebhookResponse): pass
class  DeleteRepoWebhook(WriteResponses, DeleteRepoWebhookResponse): pass

  # ==== ALERTER ====
class  CreateAlerter(WriteResponses, Alerter): pass
class  CopyAlerter(WriteResponses, Alerter): pass
class  DeleteAlerter(WriteResponses, Alerter): pass
class  UpdateAlerter(WriteResponses, Alerter): pass
class  RenameAlerter(WriteResponses, Update): pass

  # ==== PROCEDURE ====
class  CreateProcedure(WriteResponses, Procedure): pass
class  CopyProcedure(WriteResponses, Procedure): pass
class DeleteProcedure(WriteResponses, Procedure): pass
class  UpdateProcedure(WriteResponses, Procedure): pass
class  RenameProcedure(WriteResponses, Update): pass

  # ==== ACTION ====
class  CreateAction(WriteResponses, Action): pass
class  CopyAction(WriteResponses, Action): pass
class  DeleteAction(WriteResponses, Action): pass
class  UpdateAction(WriteResponses, Action): pass
class  RenameAction(WriteResponses, Update): pass

  # ==== SYNC ====
class  CreateResourceSync(WriteResponses, ResourceSync): pass
class  CopyResourceSync(WriteResponses, ResourceSync): pass
class  DeleteResourceSync(WriteResponses, ResourceSync): pass
class  UpdateResourceSync(WriteResponses, ResourceSync): pass
class  RenameResourceSync(WriteResponses, Update): pass
class  CommitSync(WriteResponses, ResourceSync): pass
class  WriteSyncFileContents(WriteResponses, Update): pass
class  RefreshResourceSyncPending(WriteResponses, ResourceSync): pass
class  CreateSyncWebhook(WriteResponses, CreateSyncWebhookResponse): pass
class  DeleteSyncWebhook(WriteResponses, DeleteSyncWebhookResponse): pass

  # ==== TAG ====
class  CreateTag(WriteResponses, Tag): pass
class  DeleteTag(WriteResponses, Tag): pass
class  RenameTag(WriteResponses, Tag): pass
class  UpdateTagColor(WriteResponses, Tag): pass
class  UpdateTagsOnResource(WriteResponses, UpdateTagsOnResourceResponse): pass

  # ==== VARIABLE ====
class  CreateVariable(WriteResponses, CreateVariableResponse): pass
class  UpdateVariableValue(WriteResponses, UpdateVariableValueResponse): pass
class  UpdateVariableDescription(WriteResponses, UpdateVariableDescriptionResponse): pass
class  UpdateVariableIsSecret(WriteResponses, UpdateVariableIsSecretResponse): pass
class  DeleteVariable(WriteResponses, DeleteVariableResponse): pass

  # ==== PROVIDERS ====
class  CreateGitProviderAccount(WriteResponses, CreateGitProviderAccountResponse): pass
class  UpdateGitProviderAccount(WriteResponses, UpdateGitProviderAccountResponse): pass
class  DeleteGitProviderAccount(WriteResponses, DeleteGitProviderAccountResponse): pass
class  CreateDockerRegistryAccount(WriteResponses, CreateDockerRegistryAccountResponse): pass
class  UpdateDockerRegistryAccount(WriteResponses, UpdateDockerRegistryAccountResponse): pass
class  DeleteDockerRegistryAccount(WriteResponses, DeleteDockerRegistryAccountResponse): pass



class ExecuteResponses: pass

  # ==== SERVER ====
class  StartContainer(ExecuteResponses, Update): pass
class  RestartContainer(ExecuteResponses, Update): pass
class  PauseContainer(ExecuteResponses, Update): pass
class UnpauseContainer(ExecuteResponses, Update): pass
class  StopContainer(ExecuteResponses, Update): pass
class  DestroyContainer(ExecuteResponses, Update): pass
class  StartAllContainers(ExecuteResponses, Update): pass
class  RestartAllContainers(ExecuteResponses, Update): pass
class  PauseAllContainers(ExecuteResponses, Update): pass
class  UnpauseAllContainers(ExecuteResponses, Update): pass
class  StopAllContainers(ExecuteResponses, Update): pass
class  PruneContainers(ExecuteResponses, Update): pass
class  DeleteNetwork(ExecuteResponses, Update): pass
class  PruneNetworks(ExecuteResponses, Update): pass
class  DeleteImage(ExecuteResponses, Update): pass
class  PruneImages(ExecuteResponses, Update): pass
class  DeleteVolume(ExecuteResponses, Update): pass
class  PruneVolumes(ExecuteResponses, Update): pass
class  PruneDockerBuilders(ExecuteResponses, Update): pass
class  PruneBuildx(ExecuteResponses, Update): pass
class  PruneSystem(ExecuteResponses, Update): pass

  # ==== STACK ====
class  DeployStack(ExecuteResponses, Update): pass
class  BatchDeployStack(ExecuteResponses, BatchExecutionResponse): pass
class  DeployStackIfChanged(ExecuteResponses, Update): pass
class  BatchDeployStackIfChanged(ExecuteResponses, BatchExecutionResponse): pass
class  PullStack(ExecuteResponses, Update): pass
class  BatchPullStack(ExecuteResponses, BatchExecutionResponse): pass
class  StartStack(ExecuteResponses, Update): pass
class  RestartStack(ExecuteResponses, Update): pass
class  StopStack(ExecuteResponses, Update): pass
class  PauseStack(ExecuteResponses, Update): pass
class  UnpauseStack(ExecuteResponses, Update): pass
class  DestroyStack(ExecuteResponses, Update): pass
class  BatchDestroyStack(ExecuteResponses, BatchExecutionResponse): pass

  # ==== DEPLOYMENT ====
class  Deploy(ExecuteResponses, Update): pass
class  BatchDeploy(ExecuteResponses, BatchExecutionResponse): pass
class  PullDeployment(ExecuteResponses, Update): pass
class  StartDeployment(ExecuteResponses, Update): pass
class  RestartDeployment(ExecuteResponses, Update): pass
class  PauseDeployment(ExecuteResponses, Update): pass
class  UnpauseDeployment(ExecuteResponses, Update): pass
class  StopDeployment(ExecuteResponses, Update): pass
class  DestroyDeployment(ExecuteResponses, Update): pass
class  BatchDestroyDeployment(ExecuteResponses, BatchExecutionResponse): pass

  # ==== BUILD ====
class  RunBuild(ExecuteResponses, Update): pass
class  BatchRunBuild(ExecuteResponses, BatchExecutionResponse): pass
class  CancelBuild(ExecuteResponses, Update): pass

  # ==== REPO ====
class  CloneRepo(ExecuteResponses, Update): pass
class  BatchCloneRepo(ExecuteResponses, BatchExecutionResponse): pass
class  PullRepo(ExecuteResponses, Update): pass
class  BatchPullRepo(ExecuteResponses, BatchExecutionResponse): pass
class  BuildRepo(ExecuteResponses, Update): pass
class  BatchBuildRepo(ExecuteResponses, BatchExecutionResponse): pass
class  CancelRepoBuild(ExecuteResponses, Update): pass

  # ==== PROCEDURE ====
class  RunProcedure(ExecuteResponses, Update): pass
class  BatchRunProcedure(ExecuteResponses, BatchExecutionResponse): pass

  # ==== ACTION ====
class  RunAction(ExecuteResponses, Update): pass
class  BatchRunAction(ExecuteResponses, BatchExecutionResponse): pass

  # ==== SYNC ====
class  RunSync(ExecuteResponses, Update): pass

  # ==== STACK Service ====
class  DeployStackService(ExecuteResponses, Update): pass
class  StartStackService(ExecuteResponses, Update): pass
class  RestartStackService(ExecuteResponses, Update): pass
class  StopStackService(ExecuteResponses, Update): pass
class  PauseStackService(ExecuteResponses, Update): pass
class  UnpauseStackService(ExecuteResponses, Update): pass
class  DestroyStackService(ExecuteResponses, Update): pass

  # ==== ALERTER ====
class  TestAlerter(ExecuteResponses, Update): pass
